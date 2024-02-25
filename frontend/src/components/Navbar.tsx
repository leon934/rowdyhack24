import React from 'react';

interface NavbarProps {
    title: string;
}

const Navbar: React.FC<NavbarProps> = ({ title }) => {
    return (
        <nav className="navbar">
            <h1>{title}</h1>
            <ul className="nav-links">
                {/* Add more links as needed */}
            </ul>
        </nav>
    );
};

export default Navbar;