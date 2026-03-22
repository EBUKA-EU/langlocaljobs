import React from "react";

function Footer() {
    return (
        <footer className="bg-gray-100 text-gray-600 text-center py-4 mt-12 border-t">
            <div className="container mx-auto">
                &copy; {new Date().getFullYear()} LangLocalJobs. All rights
                reserved.
            </div>
        </footer>
    );
}

export default Footer;
