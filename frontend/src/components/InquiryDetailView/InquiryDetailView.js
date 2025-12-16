import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import './InquiryDetailView.css';

const InquiryDetailView = () => {
    const { id } = useParams();
    const [inquiry, setInquiry] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [response, setResponse] = useState('');

    useEffect(() => {
        const fetchInquiry = async () => {
            try {
                const res = await fetch(`${process.env.REACT_APP_BACKEND_URL || ''}/api/inquiries/${id}`);
                if (!res.ok) {
                    throw new Error(`HTTP error! status: ${res.status}`);
                }
                const data = await res.json();
                setInquiry(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchInquiry();
    }, [id]);

    const handleResponseSubmit = async (e) => {
        e.preventDefault();
        if (!response.trim()) {
            alert("Response cannot be empty.");
            return;
        }

        try {
            const res = await fetch(`${process.env.REACT_APP_BACKEND_URL || ''}/api/inquiries/${id}/respond`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ response }),
            });

            if (!res.ok) {
                throw new Error(`HTTP error! status: ${res.status}`);
            }

            alert("Response submitted successfully!");
            setResponse('');

        } catch (err) {
            setError(err.message);
            alert("Failed to submit response.");
        }
    };

    if (loading) return <div className="loading-message">Loading inquiry details...</div>;
    if (error) return <div className="error-message">Error: {error}</div>;
    if (!inquiry) return <div className="loading-message">Inquiry not found.</div>;

    return (
        <div className="inquiry-detail-container">
            <h2 className="inquiry-detail-header">Inquiry #{inquiry.id}</h2>
            
            <div className="inquiry-info-grid">
                <div className="info-item">
                    <strong>Name</strong>
                    <span>{inquiry.name}</span>
                </div>
                <div className="info-item">
                    <strong>Email</strong>
                    <span>{inquiry.email}</span>
                </div>
                <div className="info-item">
                    <strong>Category</strong>
                    <span>{inquiry.category}</span>
                </div>
                <div className="info-item">
                    <strong>Urgency</strong>
                    <span>
                        <span className={`urgency-icon urgency-icon-${inquiry.urgency.toLowerCase()}`}></span>
                        {inquiry.urgency}
                    </span>
                </div>
                <div className="info-item">
                    <strong>Created At</strong>
                    <span>{new Date(inquiry.created_at).toLocaleString()}</span>
                </div>
            </div>

            <div className="inquiry-text-section">
                <h3>Full Inquiry Text</h3>
                <p className="inquiry-text">{inquiry.inquiry}</p>
            </div>

            <div className="response-section">
                <h3>Respond to Inquiry</h3>
                <form onSubmit={handleResponseSubmit}>
                    <textarea
                        className="response-textarea"
                        value={response}
                        onChange={(e) => setResponse(e.target.value)}
                        placeholder="Type your response here..."
                        required
                    />
                    <button type="submit" className="submit-response-btn">
                        Send
                    </button>
                </form>
            </div>
        </div>
    );
};

export default InquiryDetailView;