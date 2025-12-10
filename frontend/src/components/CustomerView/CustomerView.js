import React, { useState } from 'react';
import './CustomerView.css';

const CustomerView = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    inquiry: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/inquiries', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      if (response.ok) {
        alert('Inquiry submitted successfully!');
        setFormData({ name: '', email: '', inquiry: '' }); // Clear form
      } else {
        alert('Failed to submit inquiry. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting inquiry:', error);
      alert('An error occurred. Please try again later.');
    }
  };

  return (
    <div className="customer-view-container">
      <h1 className="page-title">Customer Support Inquiry</h1>

      <div className="inquiry-form-section">
        <h2 className="section-title">Submit Your Inquiry</h2>
        <form onSubmit={handleSubmit} className="inquiry-form">
          <div className="form-group">
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="inquiry">Your Inquiry:</label>
            <textarea
              id="inquiry"
              name="inquiry"
              value={formData.inquiry}
              onChange={handleChange}
              rows="5"
              required
            ></textarea>
          </div>
          <button type="submit" className="submit-button">
            Submit Inquiry
          </button>
        </form>
      </div>

      <div className="faq-section">
        <h2 className="section-title">Frequently Asked Questions</h2>
        <div className="faq-list">
          <div className="faq-item">
            <h3 className="faq-question">Q: How do I reset my password?</h3>
            <p className="faq-answer">A: You can reset your password by clicking on the "Forgot Password" link on the login page and following the instructions.</p>
          </div>
          <div className="faq-item">
            <h3 className="faq-question">Q: Where can I find my order history?</h3>
            <p className="faq-answer">A: Your order history is available in your account dashboard under the "My Orders" section.</p>
          </div>
          <div className="faq-item">
            <h3 className="faq-question">Q: How long does shipping take?</h3>
            <p className="faq-answer">A: Standard shipping usually takes 5-7 business days. Expedited options are available at checkout.</p>
          </div>
          <div className="faq-item">
            <h3 className="faq-question">Q: Can I change my delivery address after placing an order?</h3>
            <p className="faq-answer">A: Please contact our support team immediately if you need to change your delivery address. Changes are not guaranteed once an order has shipped.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CustomerView;
