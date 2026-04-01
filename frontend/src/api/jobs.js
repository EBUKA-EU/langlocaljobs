const API_BASE = "http://127.0.0.1:5000";

export const fetchAppliedJobs = async (token) => {
    const response = await fetch(`${API_BASE}/api/jobs/applied`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch applied jobs");
    return response.json();
};

export const markApplied = async (token, jobId) => {
    const response = await fetch(`${API_BASE}/api/jobs/${jobId}/apply`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to mark job as applied");
    return response.json();
};

export const fetchSavedJobs = async (token) => {
    const response = await fetch(`${API_BASE}/api/jobs/saved`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch saved jobs");
    return response.json();
};

export const saveJob = async (token, jobId) => {
    const response = await fetch(`${API_BASE}/api/jobs/${jobId}/save`, {
        method: "POST",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to save job");
    return response.json();
};

export const unsaveJob = async (token, jobId) => {
    const response = await fetch(`${API_BASE}/api/jobs/${jobId}/save`, {
        method: "DELETE",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to unsave job");
    return response.json();
};

export const fetchJobs = async (
    token,
    page = 1,
    perPage = 10,
    filters = {},
) => {
    const params = new URLSearchParams({ page, per_page: perPage });
    if (filters.search) params.set("search", filters.search);
    if (filters.location) params.set("location", filters.location);
    if (filters.company) params.set("company", filters.company);
    if (filters.date_from) params.set("date_from", filters.date_from);
    if (filters.date_to) params.set("date_to", filters.date_to);
    const response = await fetch(`${API_BASE}/api/jobs?${params.toString()}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch jobs");
    return response.json();
};

export const fetchJobById = async (token, jobId) => {
    const response = await fetch(`${API_BASE}/api/jobs/${jobId}`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!response.ok) throw new Error("Failed to fetch job details");
    return response.json();
};
