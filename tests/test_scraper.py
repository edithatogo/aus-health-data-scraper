"""Offline compatibility checks for bounded legacy scraper calls."""

import asyncio

import requests
from src.scraper import scrape_items, scrape_participants


def test_scraper_offloads_bounded_requests(monkeypatch, tmp_path):
    calls = []

    def get(url, *, timeout):
        calls.append((url, timeout))
        response = requests.Response()
        response.status_code = 200
        response._content = b"synthetic fixture"
        return response

    monkeypatch.setattr(requests, "get", get)
    asyncio.run(scrape_items(["104"], [202401], tmp_path))
    asyncio.run(scrape_participants([202401], tmp_path))
    assert len(calls) == 2
    assert all(timeout == 30 for _, timeout in calls)
    assert (tmp_path / "item_104_202401.html").read_bytes() == b"synthetic fixture"
    assert (tmp_path / "participants_202401.html").read_bytes() == b"synthetic fixture"
