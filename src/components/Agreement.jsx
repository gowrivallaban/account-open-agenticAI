import React from 'react';

const TERMS_TEXT = `
APEX FINANCIAL — CHECKING ACCOUNT TERMS & CONDITIONS

Effective Date: January 1, 2026

1. ACCOUNT AGREEMENT
By opening a checking account with GPS Financial ("Bank"), you ("Account Holder") agree to the following terms and conditions. This Agreement governs your use of the checking account and related services.

2. ELIGIBILITY
You must be at least 18 years of age and a legal U.S. resident to open an account. The Bank reserves the right to verify your identity and may decline to open an account at its sole discretion.

3. ACCOUNT OWNERSHIP
The account will be held in the name(s) provided during the application process. You are responsible for ensuring all information provided is accurate and current.

4. DEPOSITS AND WITHDRAWALS
Deposits may be made via direct deposit, mobile check deposit, wire transfer, or at any GPS Financial branch. Withdrawals can be made via debit card, ATM, online transfer, or check. Daily withdrawal limits may apply.

5. FEES AND CHARGES
- Monthly Maintenance Fee: $0.00
- ATM Fees (non-network): $0.00 (unlimited reimbursements)
- Overdraft Fee: $0.00 (we do not charge overdraft fees)
- Wire Transfer (domestic): $15.00
- Wire Transfer (international): $30.00

6. ELECTRONIC COMMUNICATIONS
By opening this account, you consent to receive account statements, notices, and disclosures electronically. You may opt out of electronic communications at any time by contacting customer service.

7. PRIVACY POLICY
Your personal information, including your Social Security Number, will be securely stored and used solely for account verification, regulatory compliance, and fraud prevention. We will not sell your personal information to third parties.

8. FDIC INSURANCE
Deposits at GPS Financial are insured by the Federal Deposit Insurance Corporation (FDIC) up to $250,000 per depositor, per ownership category.

9. ACCOUNT CLOSURE
You may close your account at any time by contacting customer service. The Bank reserves the right to close your account with 30 days' written notice.

10. GOVERNING LAW
This Agreement shall be governed by the laws of the State of Delaware and applicable federal law.

11. DISPUTE RESOLUTION
Any disputes arising from this Agreement shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association.

By clicking "I Agree" or typing "I agree", you acknowledge that you have read, understood, and agree to be bound by these Terms and Conditions.
`;

export default function Agreement({ onAgree, onDecline }) {
    return (
        <div>
            <div className="agreement-box">
                <h5>📜 Terms & Conditions</h5>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                    {TERMS_TEXT.trim()}
                </pre>
            </div>
            <div className="agreement-buttons">
                <button className="agree-btn decline" onClick={onDecline}>
                    Decline
                </button>
                <button className="agree-btn accept" onClick={onAgree}>
                    ✓ I Agree
                </button>
            </div>
        </div>
    );
}
