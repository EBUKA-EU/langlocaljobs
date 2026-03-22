import React from "react";

function SideBar({ selected, onSelect }) {
    return (
        <aside className="hidden md:block w-56 bg-gray-100 p-4 rounded shadow h-full">
            <nav className="flex flex-col gap-4">
                <button
                    className={`text-left px-2 py-1 rounded ${selected === "saved" ? "bg-blue-200 font-bold" : "hover:bg-blue-50"}`}
                    onClick={() => onSelect("saved")}
                >
                    Saved Jobs
                </button>
                <button
                    className={`text-left px-2 py-1 rounded ${selected === "applied" ? "bg-blue-200 font-bold" : "hover:bg-blue-50"}`}
                    onClick={() => onSelect("applied")}
                >
                    Applied Jobs
                </button>
            </nav>
        </aside>
    );
}

export default SideBar;
