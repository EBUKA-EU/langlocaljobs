import React from "react";

export function InputField({
    label,
    type = "text",
    name,
    value,
    onChange,
    error,
    ...props
}) {
    return (
        <div className="mb-4">
            <label className="block mb-1 font-medium" htmlFor={name}>
                {label}
            </label>
            <input
                className={`w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400 ${error ? "border-red-500" : "border-gray-300"}`}
                type={type}
                id={name}
                name={name}
                value={value}
                onChange={onChange}
                {...props}
            />
            {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
        </div>
    );
}
