import React from "react";
import { Link } from "react-router-dom";
function Home() {
    return (
        <div className="max-w-3xl mx-auto mt-12 text-center">
            <h1 className="text-4xl font-extrabold mb-4 text-blue-700">
                Welcome to LangLocalJobs
            </h1>
            <p className="mb-4 text-lg text-gray-700">
                Your gateway to language and localization careers. Discover
                opportunities, connect with recruiters, and grow your career in
                the language industry.
            </p>
            <div className="flex flex-col md:flex-row justify-center gap-8 mt-10">
                <div className="bg-white rounded shadow p-6 flex-1">
                    <h2 className="text-2xl font-bold mb-2 text-blue-600">
                        For Job Seekers
                    </h2>
                    <ul className="text-left list-disc list-inside text-gray-700">
                        <li>
                            Browse curated jobs in translation, localization,
                            and linguistics
                        </li>
                        <li>Connect with top recruiters in the industry</li>
                        <li>Easy application process</li>
                    </ul>
                </div>
                <div className="bg-white rounded shadow p-6 flex-1">
                    <h2 className="text-2xl font-bold mb-2 text-blue-600">
                        For Recruiters
                    </h2>
                    <ul className="text-left list-disc list-inside text-gray-700">
                        <li>Post jobs and reach qualified candidates</li>
                        <li>Manage applications efficiently</li>
                        <li>Build your employer brand</li>
                    </ul>
                </div>
            </div>
            <div className="mt-10 text-gray-600">
                <p>
                    Ready to get started?{" "}
                    <Link
                        to="/register"
                        className="font-semibold text-blue-700 underline hover:text-blue-900"
                    >
                        Register
                    </Link>{" "}
                    or{" "}
                    <Link
                        to="/login"
                        className="font-semibold text-blue-700 underline hover:text-blue-900"
                    >
                        Login
                    </Link>{" "}
                    to access all features!
                </p>
            </div>
        </div>
    );
}

export default Home;
