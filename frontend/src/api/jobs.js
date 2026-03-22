export const fetchJobs = async (token, page = 1, perPage = 10) => {
    const params = new URLSearchParams({ page, per_page: perPage });
    const response = await fetch(`http://127.0.0.1:5000/api/jobs?${params.toString()}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch jobs");
    return response.json();
};

export const fetchJobById = async (token, jobId) => {
    const response = await fetch(`http://127.0.0.1:5000/api/jobs/${jobId}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch job details");
    return response.json();
};
