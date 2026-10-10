import time

def wait_for_completion(client, job_id):
    for _ in range(50):
        response = client.get(f"/api/v1/certificate-jobs/{job_id}"); data = response.json()
        if data["status"] in {"completed", "completed_with_errors", "failed"}: return data
        time.sleep(0.02)
    raise AssertionError("job did not finish")

def test_bulk_generation_and_download(client):
    response = client.post("/api/v1/certificate-jobs", json={"coursename":"Python Backend","issuedate":"2026-10-10","recipients":[{"name":"Aarav Sharma","email":"aarav@example.com"},{"name":"Maya Rao","email":"maya@example.com"}]})
    assert response.status_code == 202; job = wait_for_completion(client, response.json()["job_id"]); assert job["successful_count"] == 2 and job["progress_percentage"] == 100
    results = client.get(job["results_url"]).json(); assert len(results["items"]) == 2
    pdf = client.get(f"/api/v1/certificates/{results['items'][0]['certificate_id']}"); assert pdf.status_code == 200 and pdf.content.startswith(b"%PDF")

def test_validation_and_duplicate_policy(client):
    assert client.post("/api/v1/certificate-jobs", json={"coursename":"x","issuedate":"2026-01-01","recipients":[]}).status_code == 422
    duplicate = {"coursename":"x","issuedate":"2026-01-01","recipients":[{"name":"A","email":"A@example.com"},{"name":"B","email":"a@example.com"}]}
    assert client.post("/api/v1/certificate-jobs", json=duplicate).status_code == 422

def test_missing_resources(client):
    assert client.get("/api/v1/certificate-jobs/not-a-job").status_code == 404
    assert client.get("/api/v1/certificates/unknown").status_code == 404
    assert client.get("/health").json() == {"status":"ok"}
