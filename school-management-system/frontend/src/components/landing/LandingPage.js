import React, { useEffect, useState } from 'react';
import Hero from './Hero';
import AboutUs from './AboutUs';
import NewsFeed from './NewsFeed';
import Contact from './Contact';
import './LandingPage.css'; // Add a CSS file for styling

const LandingPage = () => {
    const [activeSection, setActiveSection] = useState('hero');

    useEffect(() => {
        const handleScroll = () => {
            const sections = ['hero', 'about-us', 'news-feed', 'contact'];
            const scrollPosition = window.scrollY + window.innerHeight / 2;

            for (const section of sections) {
                const element = document.getElementById(section);
                if (element) {
                    const { offsetTop, offsetHeight } = element;
                    if (scrollPosition >= offsetTop && scrollPosition < offsetTop + offsetHeight) {
                        setActiveSection(section);
                        break;
                    }
                }
            }
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <div>
            <nav className="navbar">
                <ul className="navbar-links">
                    <li className={activeSection === 'hero' ? 'active' : ''}>
                        <a href="#hero">Home</a>
                    </li>
                    <li className={activeSection === 'about-us' ? 'active' : ''}>
                        <a href="#about-us">About Us</a>
                    </li>
                    <li className={activeSection === 'news-feed' ? 'active' : ''}>
                        <a href="#news-feed">News</a>
                    </li>
                    <li className={activeSection === 'contact' ? 'active' : ''}>
                        <a href="#contact">Contact</a>
                    </li>
                </ul>
            </nav>
            <Hero />
            <AboutUs />
            <NewsFeed />
            <Contact />
            <footer className="footer">
                <p>&copy; 2023 Our School. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default LandingPage;
