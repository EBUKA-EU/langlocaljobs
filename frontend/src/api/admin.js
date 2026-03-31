const API_BASE = "http://localhost:5000/api";

export const fetchAllAppliedJobs = async (token) => {
    const response = await fetch(`${API_BASE}/admin/applied-jobs`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch applied jobs");
    return response.json();
};

export const fetchAllUsers = async (token) => {
    const response = await fetch(`${API_BASE}/users`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch users");
    return response.json();
};

export const updateUserRole = async (token, userId, role) => {
    const response = await fetch(`${API_BASE}/users/${userId}`, {
        method: "PATCH",
        headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ role }),
    });
    if (!response.ok) throw new Error("Failed to update role");
    return response.json();
};

export const deleteUser = async (token, userId) => {
    const response = await fetch(`${API_BASE}/users/${userId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to delete user");
    return response.json();
};

export const deleteJob = async (token, jobId) => {
    const response = await fetch(`${API_BASE}/jobs/${jobId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to delete job");
    return response.json();
};

export const fetchAllJobs = async (token, page = 1, perPage = 20) => {
    const params = new URLSearchParams({ page, per_page: perPage });
    const response = await fetch(`${API_BASE}/jobs?${params}`, {
        headers: { Authorization: `Bearer ${token}` },
    });
    if (!response.ok) throw new Error("Failed to fetch jobs");
    return response.json();
};
