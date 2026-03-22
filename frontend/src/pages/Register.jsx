import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import { registerUser } from "../api/auth";
import { InputField } from "../components/InputField";

function Register() {
    const navigate = useNavigate();
    const [form, setForm] = useState({
        name: "",
        email: "",
        password: "",
        confirmPassword: "",
    });
    const [errors, setErrors] = useState({});
    const [apiError, setApiError] = useState("");
    const [success, setSuccess] = useState("");

    const mutation = useMutation({
        mutationFn: registerUser,
        onSuccess: () => {
            setSuccess("Registration successful! Redirecting to login...");
            setApiError("");
            setTimeout(() => navigate("/login"), 1500);
        },
        onError: (error) => {
            setApiError(
                error?.response?.data?.message ||
                    error?.message ||
                    "Registration failed",
            );
            setSuccess("");
        },
    });

    const validate = () => {
        const errs = {};
        if (!form.name) errs.name = "Name is required";
        if (!form.email) errs.email = "Email is required";
        else if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(form.email))
            errs.email = "Invalid email";
        if (!form.password) errs.password = "Password is required";
        else if (form.password.length < 6)
            errs.password = "Password must be at least 6 characters";
        if (!form.confirmPassword)
            errs.confirmPassword = "Please confirm your password";
        else if (form.password !== form.confirmPassword)
            errs.confirmPassword = "Passwords do not match";
        setErrors(errs);
        return Object.keys(errs).length === 0;
    };

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
        setErrors({ ...errors, [e.target.name]: undefined });
        setApiError("");
        setSuccess("");
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!validate()) return;
        mutation.mutate({
            name: form.name,
            email: form.email,
            password: form.password,
        });
    };

    return (
        <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Register</h2>
            <form onSubmit={handleSubmit} noValidate>
                <InputField
                    label="Name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                    error={errors.name}
                />
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
                <InputField
                    label="Confirm Password"
                    type="password"
                    name="confirmPassword"
                    value={form.confirmPassword}
                    onChange={handleChange}
                    error={errors.confirmPassword}
                />
                {apiError && (
                    <div className="text-red-600 mb-2">{apiError}</div>
                )}
                {success && (
                    <div className="text-green-600 mb-2">{success}</div>
                )}
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 rounded font-semibold hover:bg-blue-700 transition"
                    disabled={mutation.isPending}
                >
                    {mutation.isPending ? "Registering..." : "Register"}
                </button>
            </form>
            <div className="mt-4 text-center text-gray-700">
                Already have an account?{" "}
                <Link
                    to="/login"
                    className="text-blue-600 underline hover:text-blue-800"
                >
                    Login
                </Link>
            </div>
        </div>
    );
}

export default Register;
