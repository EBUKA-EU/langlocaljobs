import React, { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "../api/auth";
import { InputField } from "../components/InputField";

function Login({ onLogin }) {
    const [form, setForm] = useState({ email: "", password: "" });
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState("");
    const navigate = useNavigate();

    const mutation = useMutation({
        mutationFn: loginUser,
        onSuccess: (data) => {
            setApiError("");
            // Store both user and token in App state
            if (onLogin)
                onLogin({
                    ...data.user,
                    token: data.token,
                });
            navigate("/dashboard");
        },
        onError: (error) => {
            setApiError(
                error?.response?.data?.message ||
                    error?.message ||
                    "Login failed",
            );
        },
    });

    const validate = () => {
        const errs = {};
        if (!form.email) errs.email = "Email is required";
        else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email))
            errs.email = "Invalid email";
        if (!form.password) errs.password = "Password is required";
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
        setErrors({ ...errors, [e.target.name]: undefined });
        setApiError("");
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!validate()) return;
        mutation.mutate(form);
    };

    return (
        <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Login</h2>
            <form onSubmit={handleSubmit} noValidate>
                <InputField
                    label="Email"
                    type="email"
                    name="email"
                    value={form.email}
                    onChange={handleChange}
                    error={errors.email}
                />
                <InputField
                    label="Password"
                    type="password"
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    error={errors.password}
                />
                {apiError && (
                    <div className="text-red-600 mb-2">{apiError}</div>
                )}
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded font-semibold hover:bg-blue-700 transition"
                    disabled={mutation.isPending}
                >
                    {mutation.isPending ? "Logging in..." : "Login"}
                </button>
            </form>
            <div className="mt-4 text-center text-gray-700">
                Don't have an account?{" "}
                <Link
                    to="/register"
                    className="text-blue-600 underline hover:text-blue-800"
                >
                    Register
                </Link>
            </div>
        </div>
    );
}

export default Login;
