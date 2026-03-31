import React from "react";
import { Link, useNavigate } from "react-router-dom";

function NavBar({ user, onLogout }) {
    const navigate = useNavigate();

    const handleFindJobs = (e) => {
        if (!user) {
            e.preventDefault();
            navigate("/login");
        }
    };

    return (
        <nav className="bg-blue-600 p-4 text-white flex gap-4 justify-between items-center">
            <div className="flex gap-4 items-center">
                <Link to="/" className="font-bold text-lg">
                    LangLocalJobs
                </Link>
                <Link to="/jobs" onClick={handleFindJobs}>
                    Find Jobs
                </Link>
            </div>
            <div className="flex gap-4 items-center">
                {!user && <Link to="/login">Login</Link>}
                {!user && <Link to="/register">Register</Link>}
                {user && <Link to="/dashboard">Dashboard</Link>}
                {user && user.role === "admin" && (
                    <Link
                        to="/admin"
                        className="bg-yellow-400 text-gray-900 px-3 py-1 rounded font-semibold hover:bg-yellow-500"
                    >
                        Admin
                    </Link>
                )}
                {user && (
                    <button
                        onClick={() => {
                            onLogout();
                            navigate("/login");
                        }}
                        className="bg-red-500 hover:bg-red-700 text-white px-3 py-1 rounded"
                    >
                        Logout
                    </button>
                )}
            </div>
        </nav>
    );
}

export default NavBar;
