# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CESNET
#
# oarepo-s3 is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Drafts integration tests."""
import io

from celery.contrib.pytest import celery_worker, celery_session_worker
from mock import patch

from tests.utils import draft_entrypoints


@patch('pkg_resources.iter_entry_points', draft_entrypoints, celery_session_worker)
def test_draft_integration(app, draft_record, client):
    """Test integration with invenio records draft library."""
    fsize = 1024 * 1024 * 200

    # Test multipart upload can be created
    resp = client.post(
        '/draft/records/1/files/?multipart=True',
        content_type='application/x-www-form-urlencoded',
        data={
            'key': 'test.txt',
            'multipart_content_type': 'text/plain',
            'size': fsize
        })
    assert resp.status_code == 201
    assert 'multipart_upload' in resp.json

    complete_url = resp.json['multipart_upload']['complete_url']
    abort_url = resp.json['multipart_upload']['abort_url']

    assert complete_url and abort_url

    # Test in-progress upload can be aborted once
    resp = client.post(abort_url)
    assert resp.status_code == 200
    assert resp.json['status'] == 'aborted'

    # Test that aborted file doesn't exist anymore
    resp = client.post(abort_url)
    assert resp.status_code == 404

    resp = client.get('/draft/records/1/files/')
    assert resp.status_code == 200
    assert len(resp.json) == 0

    # Test cannot complete aborted upload
    resp = client.post(
        complete_url,
        json=dict(
            parts=[]
        )
    )
    assert resp.status_code == 404

    # Test multipart upload complete endpoint
    resp = client.post(
        '/draft/records/1/files/?multipart=True',
        content_type='application/x-www-form-urlencoded',
        data={
            'key': 'test2.txt',
            'multipart_content_type': 'text/plain',
            'size': fsize
        })
    assert resp.status_code == 201
    complete_url = resp.json['multipart_upload']['complete_url']

    resp = client.post(
        complete_url,
        json=dict(
            parts=[]
        )
    )
    assert resp.status_code == 200
    assert 'etag:test' in resp.json['checksum']

    # Test file download redirects to s3
    resp = client.get('/draft/records/1/files/test2.txt')
    assert resp.status_code == 302
    assert resp.headers['Location'].startswith('https://s3')

    # Test file upload metadata are gone from record files resource
    resp = client.get('/draft/records/1/files/')
    assert resp.status_code == 200
    assert 'multipart_upload' not in resp.json[0]

    # Test if single-part file upload still works
    resp = client.put(
        '/draft/records/1/files/nmp.txt',
        data=io.BytesIO(b"some random data"),
        content_type='text/plain')
    assert resp.status_code == 201

    # Test complete on a non-multipart file fails
    resp = client.post(
        '/draft/records/1/files/nmp.txt/complete-multipart',
        json=dict(
            parts=[]
        ))
    assert resp.status_code == 400

    # Test complete on a non-existent file fails
    resp = client.post(
        '/draft/records/1/files/nope/complete-multipart',
        json=dict(
            parts=[]
        ))
    assert resp.status_code == 404

    # Test abort on a non-multipart file fails
    resp = client.post('/draft/records/1/files/nmp.txt/abort-multipart')
    assert resp.status_code == 400
