import React from 'react';
import { Header } from '../components/Header';
import { Footer } from '../components/Footer';
import { Shield, FileText, RefreshCw, Cookie, ScrollText, ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';

const policies = {
  terms: {
    icon: ScrollText,
    title: 'Terms of Service',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. Nature of Services', content: 'The Platform provides AI-assisted spiritual, astrological, and behavioral insights for personal reflection, emotional awareness, spiritual exploration, and personal growth. Services are interpretive and belief-based, not scientific or deterministic.' },
      { heading: '2. Not Professional Advice', content: 'Services do not constitute medical advice, psychological therapy, financial advice, or legal advice. Users are strongly encouraged to seek guidance from licensed professionals.' },
      { heading: '3. AI Output & Hallucination Risk', content: 'AI-generated outputs are probabilistic and may be incomplete, inaccurate, or outdated. They should not be relied upon as definitive statements of fact.' },
      { heading: '4. Eligibility', content: 'Users must be at least 18 years of age, possess legal capacity to enter into binding agreements, and not be restricted from accessing the Services under applicable law.' },
      { heading: '5. Account Security', content: 'Users are solely responsible for maintaining the confidentiality of their account credentials. All activity through a User\'s account is deemed authorized by that User.' },
      { heading: '6. Intellectual Property', content: 'All IP rights are owned by or licensed to SkyHound Studios. Users receive a limited, non-exclusive, non-transferable, revocable license for personal non-commercial use only.' },
      { heading: '7. Limitation of Liability', content: 'Total liability shall not exceed fees paid in the preceding 12 months or INR equivalent of USD $100. The Company is not liable for indirect damages, financial losses, or emotional outcomes.' },
      { heading: '8. Dispute Resolution', content: 'Disputes shall be resolved through binding arbitration seated in Delhi, India, conducted in English. Decisions are final and binding.' },
      { heading: '9. Governing Law', content: 'These Terms are governed by the laws of India. Users submit to the exclusive jurisdiction of courts in Delhi, India.' },
      { heading: '10. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ],
    fullText: [
      "These Terms of Service govern your access to and use of www.everydayhoroscope.in, Mobile Application Celestial AI, and all related Services provided by SkyHound Studios. By using the Services you agree to be legally bound by these Terms.",
      "DEFINITIONS: Services means all digital offerings including AI-generated insights, reports, subscriptions, consultations and marketplace products. Platform means the website, mobile apps, APIs and digital infrastructure. AI Services means automated guidance generated using machine learning and artificial intelligence.",
      "NATURE OF SERVICES: The Platform provides AI-assisted spiritual and astrological insights for personal reflection, emotional awareness, spiritual exploration and personal growth. Services are interpretive and belief-based. The Company does not guarantee accuracy or specific life outcomes.",
      "CRITICAL DISCLAIMERS: Services do not constitute medical advice, psychological therapy, financial advice, or legal advice. AI outputs may be incomplete, inaccurate or outdated. Remedies suggested are derived from cultural or traditional belief systems. The Platform does not promote any particular belief system.",
      "ELIGIBILITY: Users must be at least 18 years of age, possess legal capacity to enter binding agreements, and not be restricted from accessing the Services under applicable law.",
      "ACCOUNT REGISTRATION AND SECURITY: Users must provide accurate Registration Data. Users are solely responsible for maintaining confidentiality of credentials. All activity through a User's account is deemed authorized by that User. Accounts are personal and non-transferable.",
      "INTELLECTUAL PROPERTY: All IP rights in the Platform and Services are owned by or licensed to SkyHound Studios. Users receive a limited, non-exclusive, non-transferable, revocable license for personal non-commercial use. Users must not copy, reverse engineer, scrape, or use platform content to train AI models.",
      "PAYMENTS, SUBSCRIPTIONS AND WALLET: Subscriptions may auto-renew unless cancelled. Digital services are generally non-refundable after delivery. Wallet balances are non-transferable and non-interest bearing.",
      "ACCEPTABLE USE: Users must not extract or scrape platform data, use content to train AI models, attempt unauthorized system access, or engage in unlawful or harmful activities. Violation may result in termination and legal action.",
      "LIMITATION OF LIABILITY: The Company shall not be liable for indirect or consequential damages, financial losses from decisions based on platform insights, or emotional or psychological outcomes. Total liability shall not exceed fees paid in the preceding 12 months or INR equivalent of USD $100.",
      "INDEMNIFICATION: You agree to indemnify and hold harmless SkyHound Studios from any claims, damages, liabilities, losses, costs, or expenses arising from your violation of these Terms, applicable law, third-party rights, content you submitted, or misuse of Services.",
      "ACCOUNT SUSPENSION: The Company has the absolute right to suspend, restrict, or permanently terminate a User's access at any time, with or without prior notice, for suspected fraud, misuse, Terms violation, or activities detrimental to platform integrity.",
      "DISPUTE RESOLUTION: Disputes shall be resolved through binding arbitration. Seat and venue: Delhi, India. Language: English. Decisions are final and binding.",
      "GOVERNING LAW AND JURISDICTION: These Terms shall be governed by the laws of India. Users submit to the exclusive jurisdiction of courts in Delhi, India.",
      "CONTACT: SkyHound Studios. Email: prateekmalhotra.contentcreator@gmail.com. Effective Date: 18th February 2026. Last Updated: 18th February 2026."
    ],
  },
  privacy: {
    icon: Shield,
    title: 'Privacy Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. Data We Collect', content: 'We collect identity and contact information, astrological and spiritual data (date, time, place of birth), behavioral and interaction data, AI interaction data, transaction metadata, and device and technical data.' },
      { heading: '2. How We Use Your Data', content: 'We process data to provide personalized insights, generate AI-driven reports, improve behavioral models, process transactions, prevent fraud, conduct analytics, and enhance service quality.' },
      { heading: '3. AI Model Training', content: 'The Company may use aggregated, anonymized, or de-identified data to improve AI systems. Identifiable personal data is not used for external AI training or sale to third parties without lawful basis or explicit consent.' },
      { heading: '4. Data Sharing', content: 'We may share data with cloud infrastructure providers, payment processors, analytics platforms, and legal authorities where required. All partners are subject to contractual data protection obligations.' },
      { heading: '5. Your Rights', content: 'Users may have rights to access, correct, delete, restrict, object to processing, withdraw consent, and request data portability. Submit requests to: prateekmalhotra.contentcreator@gmail.com' },
      { heading: '6. Data Security', content: 'We implement encryption technologies, access controls, monitoring and incident detection systems, and secure hosting infrastructure.' },
      { heading: "7. Children's Privacy", content: 'Our Services are not intended for individuals under the age of 18. We do not knowingly collect personal data from minors.' },
      { heading: '8. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ],
    fullText: [
      "This Privacy Policy describes how SkyHound Studios collects, uses, stores, processes, shares, and safeguards personal data when you access or use www.everydayhoroscope.in, Mobile Application Celestial AI, and all related services.",
      "DATA WE COLLECT — Identity and Contact: Name, email address, phone number, country or general location, and profile information voluntarily provided.",
      "DATA WE COLLECT — Astrological and Spiritual: Date, time, and place of birth, personal reflections or journaling inputs, spiritual preferences or belief indicators, and manifestation goals or intentions. This category may be treated as sensitive personal data.",
      "DATA WE COLLECT — Behavioural and Interaction: App usage patterns, clickstream data, session duration, notification engagement behavior, emotional inputs or mood-tracking indicators, and feature interaction history.",
      "DATA WE COLLECT — AI Interaction: User queries and prompts, generated responses, contextual signals used to improve interactions, and behavioral inference outputs.",
      "DATA WE COLLECT — Transaction and Technical: We do not store full card numbers or payment credentials. We retain limited transactional metadata for accounting and fraud prevention. Technical data includes IP address, device type, operating system version, network information, and cookies.",
      "LEGAL BASIS FOR PROCESSING: User consent, contractual necessity for service delivery, legitimate business interests, and compliance with legal obligations. Sensitive personal data is processed only with explicit consent.",
      "AI MODEL TRAINING AND DATA USE: The Company may use aggregated, anonymized, de-identified, or pseudonymized data to improve AI systems. The Company does not use identifiable personal data for external AI training or sale to third parties without lawful basis or explicit consent.",
      "DATA SHARING AND THIRD-PARTY PROCESSORS: We may share data with cloud infrastructure providers, payment processors, analytics platforms, customer support tools, and legal authorities where required. All partners are subject to contractual data protection obligations.",
      "DATA RETENTION: Data is retained only as long as necessary to provide Services, comply with legal obligations, and prevent fraud. Users may request deletion subject to legal retention requirements.",
      "USER RIGHTS: Access, correct, delete, restrict, object to processing, withdraw consent, and request data portability. Submit requests to prateekmalhotra.contentcreator@gmail.com.",
      "DATA SECURITY: Encryption technologies, access controls, monitoring and incident detection systems, and secure hosting infrastructure. No digital system can be guaranteed completely secure.",
      "CHILDREN'S PRIVACY: Our Services are not intended for individuals under 18. We do not knowingly collect personal data from minors.",
      "CONTACT: SkyHound Studios. Email: prateekmalhotra.contentcreator@gmail.com. Effective Date: 18th February 2026. Last Updated: 18th February 2026."
    ],
  },
  'subscription-terms': {
    icon: FileText,
    title: 'Subscription Terms',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. Subscription Services', content: 'Plans may provide access to daily, weekly, and monthly astrological insights, AI-generated spiritual guidance, personalized reports, manifestation programs, emotional trend analysis, and compatibility insights.' },
      { heading: '2. Billing & Payment', content: 'Subscription fees may be charged on a recurring monthly, quarterly, or annual basis. By subscribing, Users authorize automatic charges in accordance with the selected billing cycle.' },
      { heading: '3. Auto-Renewal', content: 'Unless cancelled before the end of the billing period, subscriptions automatically renew. Users are responsible for monitoring subscription status and cancelling prior to the next billing cycle.' },
      { heading: '4. Free Trials', content: 'Where provided, subscriptions automatically convert to paid plans upon trial expiry unless cancelled in advance. Each User is eligible for only one free trial per offering.' },
      { heading: '5. Cancellation', content: 'Users may cancel at any time through account settings or customer support. Cancellation prevents future billing but does not entitle the User to refunds for the current billing period.' },
      { heading: '6. Refunds', content: 'Subscription fees are generally non-refundable once charged, except where required by applicable consumer protection laws or in cases of verified billing errors.' },
      { heading: '7. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ],
    fullText: [
      "These Subscription Terms govern all recurring paid services and subscription-based offerings provided by SkyHound Studios through www.everydayhoroscope.in and Mobile Application Celestial AI.",
      "SUBSCRIPTION SERVICES: Plans may provide access to daily, weekly, and monthly astrological insights, AI-generated spiritual guidance, personalized reports, manifestation programs, emotional or behavioral trend analysis, compatibility or relationship insights, and premium content. All content is for informational, experiential, and reflective purposes only.",
      "BILLING AND PAYMENT: Fees may be charged on a monthly, quarterly, or annual recurring basis through third-party payment gateways, mobile platform billing systems, or in-app wallet mechanisms. By subscribing, Users authorize automatic charges. Users must maintain valid payment methods at all times.",
      "AUTO-RENEWAL: Unless cancelled before the end of the billing period, subscriptions automatically renew for successive periods of the same duration. Users are responsible for monitoring subscription status and cancelling prior to the next billing cycle.",
      "FREE TRIALS: Where provided, trial duration will be clearly disclosed. Subscriptions automatically convert to paid plans upon trial expiry unless cancelled in advance. Each User is eligible for only one free trial per offering unless otherwise stated.",
      "PRICE CHANGES: The Company reserves the right to modify pricing to reflect changes in service offerings, operational costs, market conditions, or regulatory requirements. Changes typically take effect from the next renewal cycle.",
      "CANCELLATION: Users may cancel through account settings, app store tools, or customer support. Cancellation prevents future billing but does not entitle the User to refunds for the current billing period.",
      "REFUNDS: Subscription fees are generally non-refundable once charged, except where required by applicable consumer protection laws, in cases of verified billing errors, or where substantial service outages prevent access for a material period.",
      "ACCOUNT SHARING: Subscriptions are personal, non-transferable, and non-assignable. Unauthorized sharing, resale, or commercial use may result in suspension or termination without refund.",
      "LIMITATION OF LIABILITY: The Company shall not be liable for emotional reliance on subscription content, financial decisions influenced by insights, or perceived lack of spiritual outcomes.",
      "GOVERNING LAW: These Subscription Terms shall be governed by the laws of India. Disputes fall under the jurisdiction of courts in Delhi.",
      "CONTACT: SkyHound Studios. Email: prateekmalhotra.contentcreator@gmail.com. Effective Date: 18th February 2026. Last Updated: 18th February 2026."
    ],
  },
  'refund-policy': {
    icon: RefreshCw,
    title: 'Refund & Cancellation Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. General No-Refund Principle', content: 'Purchases are final and non-refundable once digital content is accessed or delivered, reports are generated, consultations are initiated, the subscription billing cycle begins, or spiritual services are fulfilled.' },
      { heading: '2. Eligible Refund Scenarios', content: 'Refunds may be considered only for duplicate payments, technical failure or non-delivery (notify within 24 hours), and consultation wallet deduction errors (notify within 24 hours).' },
      { heading: '3. Two-Hour Cancellation Window', content: 'Refund requests may be considered if the User emails the Company within 2 hours of payment AND the service has not yet been accessed, initiated, or fulfilled.' },
      { heading: '4. Subscriptions', content: 'Cancellation prevents future billing only. Current billing cycle remains non-refundable. Free trials convert automatically to paid subscriptions unless cancelled before expiry.' },
      { heading: '5. Refund Processing', content: 'Approved refunds will be processed within 7 business days via the original payment method. Transaction fees or service delivery costs may be deducted.' },
      { heading: '6. Spiritual Outcomes', content: 'No refund shall be granted due to lack of perceived spiritual effectiveness, emotional dissatisfaction, differences in belief systems, or unmet life outcome expectations.' },
      { heading: '7. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ],
    fullText: [
      "This Refund and Cancellation Policy governs all purchases made through www.everydayhoroscope.in and Mobile Application Celestial AI, operated by SkyHound Studios.",
      "GENERAL NO-REFUND PRINCIPLE: Except where required by applicable law, purchases are final and non-refundable once digital content is accessed or delivered, reports are generated, consultations are initiated, the subscription billing cycle begins, or spiritual services are fulfilled. Dissatisfaction with predictions, interpretations, or spiritual outcomes does not qualify for refund.",
      "ELIGIBLE REFUND SCENARIOS — Duplicate Payment: Where a User is charged more than once for the same transaction, one payment may be refunded after verification.",
      "ELIGIBLE REFUND SCENARIOS — Technical Failure or Non-Delivery: If payment has been successfully completed but service was not delivered due to technical or system error, the User must notify the Company within 24 hours.",
      "ELIGIBLE REFUND SCENARIOS — Consultation Wallet Deduction Error: Where wallet balance is deducted due to technical malfunction but the consultation does not occur at all, the User must notify the Company within 24 hours. Wallet balances are non-transferable, non-refundable, and intended solely for use within the Platform.",
      "DIGITAL REPORTS AND PERSONALIZED SERVICES: No refund where incorrect or incomplete data was provided by the User. Once report generation begins, the service is deemed delivered. Consultations are non-refundable once initiated.",
      "TWO-HOUR CANCELLATION WINDOW: Refund requests may be considered if the User emails the Company within 2 hours of payment AND the Paid Service has not yet been accessed, initiated, or fulfilled.",
      "SUBSCRIPTIONS: Cancellation prevents future billing only. Current billing cycle remains non-refundable. Free trials convert automatically to paid subscriptions unless cancelled before expiry.",
      "MARKETPLACE PRODUCTS: Physical products are eligible for replacement only where damaged, defective, incorrect, or with material portion missing. Users must notify within 2 working days with photographic evidence.",
      "SPIRITUAL AND REMEDY OUTCOME DISCLAIMER: No refund shall be granted due to lack of perceived spiritual effectiveness, emotional dissatisfaction, differences in belief systems, or unmet life outcome expectations.",
      "REFUND PROCESSING: Approved refunds will be processed within 7 business days via the original payment method. Transaction fees, gateway charges, or service delivery costs may be deducted.",
      "CHARGEBACK AND FRAUD PREVENTION: Initiating a chargeback without first contacting support may result in account suspension. Fraudulent refund claims may result in legal action.",
      "CONTACT: SkyHound Studios. Email: prateekmalhotra.contentcreator@gmail.com. Effective Date: 18th February 2026. Last Updated: 18th February 2026."
    ],
  },
  'cookie-policy': {
    icon: Cookie,
    title: 'Cookie Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. What Are Cookies', content: 'Cookies are small text files stored on your device. They enable platforms to recognize devices, remember preferences, and support functionality. We may also use local storage, pixel tags, SDK tracking tools, and device identifiers.' },
      { heading: '2. Types of Cookies We Use', content: 'We use strictly necessary cookies (authentication, security, payments), performance and analytics cookies, personalization cookies, marketing and attribution cookies, and AI and behavioral optimization signals.' },
      { heading: '3. Your Cookie Choices', content: 'Users may manage cookie preferences through browser settings, device privacy controls, or in-app consent tools. Disabling certain cookies may affect platform functionality.' },
      { heading: '4. International Users', content: 'Users in certain jurisdictions such as the EU or UK may have enhanced rights. We aim to comply with GDPR, ePrivacy Directive, and applicable global privacy regulation.' },
      { heading: '5. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ],
    fullText: [
      "This Cookie Policy explains how SkyHound Studios uses cookies and similar tracking technologies when you access or use www.everydayhoroscope.in, Mobile Application Celestial AI, and any related services. This Policy should be read together with our Privacy Policy and Terms of Service.",
      "WHAT ARE COOKIES: Cookies are small text files stored on your device when you access digital services. They enable platforms to recognize devices, remember preferences, and support functionality. We may also use local storage, pixel tags, SDK tracking tools, device identifiers, and server-side tracking mechanisms.",
      "PURPOSES FOR USING COOKIES: We use cookies to enable core platform functionality and secure authentication, deliver personalized astrological insights, remember user preferences, support AI-driven personalization, improve performance and reliability, detect and prevent fraud, measure marketing effectiveness, support analytics and product development, and optimize notification timing.",
      "STRICTLY NECESSARY COOKIES: Essential for user authentication, account session management, platform security, fraud prevention, payment transaction integrity, and system load balancing. These cookies cannot be disabled.",
      "PERFORMANCE AND ANALYTICS COOKIES: Help us understand how Users interact with the Services including feature usage patterns, navigation behavior, technical performance, and aggregate traffic trends.",
      "PERSONALIZATION COOKIES: Enable delivery of tailored experiences including customized astrological insights, behavioral recommendations, and user interface preferences and saved settings.",
      "MARKETING AND ATTRIBUTION COOKIES: Track referral sources, evaluate campaign performance, and support growth strategies. May be placed by advertising or attribution partners.",
      "AI AND BEHAVIORAL OPTIMIZATION SIGNALS: Certain tracking mechanisms support machine learning model refinement, notification timing optimization, feature recommendation systems, and platform engagement analytics.",
      "USER CONTROL AND COOKIE CHOICES: Manage cookie preferences through browser configuration settings, device privacy controls, and in-app consent or preference management tools. Disabling certain cookies may affect platform functionality.",
      "COOKIE RETENTION: Session cookies are deleted at the end of a session. Preference or analytics cookies may persist longer. We periodically review retention practices.",
      "CONSENT MANAGEMENT: Where required by applicable law, we obtain consent before deploying non-essential cookies and provide mechanisms to withdraw or modify consent at any time.",
      "INTERNATIONAL USERS: Users in the EU or UK may have enhanced rights. We aim to comply with GDPR, ePrivacy Directive, and applicable global privacy regulation.",
      "CONTACT: SkyHound Studios. Email: prateekmalhotra.contentcreator@gmail.com. Effective Date: 18th February 2026. Last Updated: 18th February 2026."
    ],
  }
};

export const PolicyPage = ({ type }) => {
  const navigate = useNavigate();
  const [showFull, setShowFull] = React.useState(false);
  const policy = policies[type];

  if (!policy) return null;
  const Icon = policy.icon;

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Header />
      <main className="flex-1 max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <Button variant="ghost" onClick={() => navigate(-1)} className="mb-6">
          <ArrowLeft className="h-4 w-4 mr-2" />Back
        </Button>

        <div className="text-center mb-10">
          <Icon className="h-12 w-12 text-gold mx-auto mb-4" />
          <h1 className="text-4xl font-playfair font-bold mb-2">{policy.title}</h1>
          <p className="text-sm text-muted-foreground">Effective Date: {policy.effective} · {policy.company}</p>
        </div>

        <div className="space-y-6">
          {policy.sections.map((section, index) => (
            <div key={index} className="p-6 rounded-xl border border-border bg-card">
              <h2 className="text-lg font-semibold mb-3 text-gold">{section.heading}</h2>
              <p className="text-muted-foreground leading-relaxed text-sm">{section.content}</p>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 rounded-xl border border-border bg-muted/20">
          <p className="text-sm text-muted-foreground text-center">
            This page contains a summary of our {policy.title}. The complete legal document is available below.
            By using Everyday Horoscope, you agree to be bound by the complete terms.
          </p>
        </div>

        <div className="mt-4">
          <button
            onClick={() => setShowFull(prev => !prev)}
            className="w-full flex items-center justify-between p-4 rounded-xl border border-gold/30 bg-gold/5 hover:bg-gold/10 transition-colors"
          >
            <span className="text-sm font-medium text-gold">
              {showFull ? 'Hide' : 'View'} Complete Legal Document
            </span>
            <span className="text-gold text-lg">{showFull ? '▲' : '▼'}</span>
          </button>

          {showFull && (
            <div className="mt-2 p-6 rounded-xl border border-border bg-card">
              <p className="text-xs text-muted-foreground mb-4">
                Effective Date: {policy.effective} · Operated by: {policy.company}
              </p>
              {policy.fullText && policy.fullText.map((para, i) => (
                <p key={i} className="text-sm text-muted-foreground leading-relaxed mb-3">{para}</p>
              ))}
            </div>
          )}
        </div>

        <div className="mt-6 p-4 rounded-xl border border-gold/20 bg-gold/5 text-center">
          <p className="text-xs text-muted-foreground">
            For questions about this policy, contact us at{' '}
            <a href="mailto:prateekmalhotra.contentcreator@gmail.com" className="text-gold hover:underline">
              prateekmalhotra.contentcreator@gmail.com
            </a>
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
};
