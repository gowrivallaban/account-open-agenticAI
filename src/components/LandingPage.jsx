import React from 'react';

export default function LandingPage({ onOpenChatbot }) {
    return (
        <>
            {/* Navbar */}
            <nav className="navbar">
                <a href="#" className="navbar-brand">
                    <span className="logo-icon">◆</span>
                    Apex Financial
                </a>
                <ul className="navbar-links">
                    <li><a href="#products">Products</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </nav>

            {/* Hero */}
            <section className="hero">
                <div className="hero-badge">
                    <span className="pulse-dot"></span>
                    AI-Powered Banking
                </div>
                <h1>
                    Banking for the <br />
                    <span className="gradient-text">Next Generation</span>
                </h1>
                <p>
                    Open accounts instantly with our AI assistant. Experience seamless,
                    secure, and intelligent banking designed for the modern world.
                </p>
                <button className="btn btn-primary" onClick={onOpenChatbot}>
                    Open a Checking Account →
                </button>
            </section>

            {/* Products */}
            <section id="products" className="products-section">
                <div className="section-header">
                    <h2>Our Products</h2>
                    <p>Choose the financial products that fit your lifestyle</p>
                </div>

                <div className="products-grid">
                    {/* Credit Cards */}
                    <div className="product-card">
                        <div className="product-card-icon purple">💳</div>
                        <h3>Credit Cards</h3>
                        <p>
                            Premium rewards and cashback credit cards with no annual fee and
                            competitive interest rates.
                        </p>
                        <ul className="features-list">
                            <li><span className="check">✓</span> Up to 3% cashback on purchases</li>
                            <li><span className="check">✓</span> No annual fee</li>
                            <li><span className="check">✓</span> 0% intro APR for 15 months</li>
                            <li><span className="check">✓</span> Fraud protection guarantee</li>
                        </ul>
                        <button className="btn btn-secondary btn-block btn-sm">Learn More</button>
                    </div>

                    {/* Checking Account */}
                    <div className="product-card" style={{ border: '1px solid rgba(20, 184, 166, 0.3)' }}>
                        <div className="product-card-icon teal">🏦</div>
                        <h3>Checking Account</h3>
                        <p>
                            Everyday checking with zero maintenance fees. Open your account
                            in minutes with our AI-powered assistant.
                        </p>
                        <ul className="features-list">
                            <li><span className="check">✓</span> No monthly maintenance fees</li>
                            <li><span className="check">✓</span> Free ATM access nationwide</li>
                            <li><span className="check">✓</span> Instant AI-assisted account opening</li>
                            <li><span className="check">✓</span> Mobile check deposit</li>
                        </ul>
                        <button
                            id="open-checking-btn"
                            className="btn btn-primary btn-block btn-sm"
                            onClick={onOpenChatbot}
                        >
                            Open Account with AI Assistant →
                        </button>
                    </div>

                    {/* Savings Account */}
                    <div className="product-card">
                        <div className="product-card-icon gold">🪙</div>
                        <h3>Savings Account</h3>
                        <p>
                            High-yield savings accounts to help your money grow faster with
                            industry-leading interest rates.
                        </p>
                        <ul className="features-list">
                            <li><span className="check">✓</span> 4.25% APY high-yield savings</li>
                            <li><span className="check">✓</span> No minimum balance required</li>
                            <li><span className="check">✓</span> FDIC insured up to $250,000</li>
                            <li><span className="check">✓</span> Automatic savings goals</li>
                        </ul>
                        <button className="btn btn-gold btn-block btn-sm">Learn More</button>
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="footer">
                <p>© 2026 Apex Financial. All rights reserved. FDIC Insured. Equal Housing Lender.</p>
            </footer>
        </>
    );
}
