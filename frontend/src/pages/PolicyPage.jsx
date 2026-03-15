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
      { heading: '1. Nature of Services', content: 'The Platform provides AI-assisted spiritual, astrological, and behavioral insights intended to support personal reflection, emotional awareness, spiritual exploration, and personal growth. The Services are interpretive, experiential, and belief-based in nature. They are not scientific or deterministic in their outcomes.' },
      { heading: '2. Not Professional Advice', content: 'The Services are provided for informational, reflective, and experiential purposes only and do not constitute medical advice or diagnosis, psychological therapy or mental health counseling, financial or investment advice, or legal advice. Users are strongly encouraged to seek guidance from licensed professionals for matters involving health, legal rights, or financial decisions.' },
      { heading: '3. AI Output & Hallucination Risk', content: 'AI-generated outputs are produced using probabilistic computational models. They may be incomplete, inaccurate, or outdated, and should not be relied upon as definitive statements of fact. Users acknowledge and accept that reliance on AI-generated insights is undertaken at their own discretion.' },
      { heading: '4. Eligibility', content: 'To use the Services, Users must be at least 18 years of age, possess legal capacity to enter into binding agreements, and not be restricted from accessing the Services under applicable law.' },
      { heading: '5. Account Security', content: 'Users are solely responsible for maintaining the confidentiality of their account credentials. All activity conducted through a User\'s account shall be deemed authorized by that User unless proven otherwise under applicable law.' },
      { heading: '6. Intellectual Property', content: 'All intellectual property rights in and to the Platform and the Services are owned by or licensed to SkyHound Studios. Users are granted a limited, non-exclusive, non-transferable, revocable license to access and use the Services solely for personal, non-commercial purposes.' },
      { heading: '7. Limitation of Liability', content: 'Total liability shall not exceed the greater of fees paid by the User in the preceding 12 months or INR equivalent of USD $100. The Company shall not be liable for indirect or consequential damages, financial losses arising from decisions based on platform insights, or emotional or psychological outcomes.' },
      { heading: '8. Dispute Resolution', content: 'Disputes shall be resolved through binding arbitration. The seat and venue of arbitration shall be Delhi, India. Proceedings shall be conducted in the English language. Arbitration decisions shall be final and binding on both parties.' },
      { heading: '9. Governing Law', content: 'These Terms shall be governed by and construed in accordance with the laws of India. Users agree to submit to the exclusive jurisdiction of courts located in Delhi, India.' },
      { heading: '10. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ]
  },
  privacy: {
    icon: Shield,
    title: 'Privacy Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. Data We Collect', content: 'We collect identity and contact information (name, email, phone), astrological and spiritual data (date, time, place of birth, spiritual preferences), behavioral and interaction data (app usage, session duration), AI interaction data (queries and responses), device and technical data (IP address, device type), and limited transactional metadata.' },
      { heading: '2. How We Use Your Data', content: 'We process personal data to provide personalized spiritual and astrological insights, generate AI-driven recommendations and reports, improve behavioral models and predictive systems, process transactions and subscriptions, prevent fraud and security incidents, and enhance overall service quality.' },
      { heading: '3. AI Model Training', content: 'To enhance the quality of our Services, the Company may use aggregated, anonymized, or de-identified data to improve AI systems. The Company does not use identifiable personal data for external AI training or sale to third parties without a lawful basis or explicit user consent.' },
      { heading: '4. Data Sharing', content: 'We may share personal data with trusted service providers including cloud infrastructure providers, payment processors, analytics platforms, and legal or regulatory authorities where required. All third-party partners are subject to contractual data protection obligations.' },
      { heading: '5. Your Rights', content: 'Depending on jurisdiction, Users may have rights to access, correct, request deletion, restrict or object to processing, withdraw consent, and request data portability. Requests may be submitted to: prateekmalhotra.contentcreator@gmail.com' },
      { heading: '6. Data Security', content: 'We implement technical and organizational safeguards including encryption technologies, access controls, monitoring and incident detection systems, and secure hosting infrastructure.' },
      { heading: '7. Children\'s Privacy', content: 'Our Services are not intended for individuals under the age of 18. We do not knowingly collect personal data from minors.' },
      { heading: '8. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ]
  },
  'subscription-terms': {
    icon: FileText,
    title: 'Subscription Terms',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. Subscription Services', content: 'Subscription plans may provide access to daily or periodic astrological insights, AI-generated spiritual or behavioral guidance, personalized reports, manifestation programs, emotional or behavioral trend analysis, and compatibility or relationship insights.' },
      { heading: '2. Billing & Payment', content: 'Subscription fees may be charged on a recurring monthly, quarterly, or annual basis. By subscribing, Users authorize the Company or its payment partners to charge the applicable subscription fees automatically in accordance with the selected billing cycle.' },
      { heading: '3. Auto-Renewal', content: 'Unless cancelled before the end of the applicable billing period, subscriptions will automatically renew for successive periods of the same duration. Users are responsible for monitoring their subscription status and cancelling prior to the next billing cycle if they do not wish to continue.' },
      { heading: '4. Free Trials', content: 'Where free trials are provided, the subscription will automatically convert into a paid plan upon expiry of the trial period unless cancelled in advance. Each User may be eligible for only one free trial per subscription offering unless otherwise stated.' },
      { heading: '5. Cancellation', content: 'Users may cancel subscriptions at any time through account settings or customer support. Cancellation will prevent future billing but will not entitle the User to refunds for the current billing period unless otherwise required by law.' },
      { heading: '6. Refunds', content: 'Subscription fees are generally non-refundable once charged, except where required by applicable consumer protection laws or in cases of verified billing errors.' },
      { heading: '7. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ]
  },
  'refund-policy': {
    icon: RefreshCw,
    title: 'Refund & Cancellation Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. General No-Refund Principle', content: 'Except where required by applicable law, purchases are final and non-refundable once digital content is accessed or delivered, reports are generated, consultations are initiated, the subscription billing cycle begins, or spiritual or ritual services are fulfilled.' },
      { heading: '2. Eligible Refund Scenarios', content: 'Refund requests may be considered only for: duplicate payments (one charge refunded after verification), technical failure or non-delivery (must notify within 24 hours), and consultation wallet deduction errors due to technical malfunction (must notify within 24 hours).' },
      { heading: '3. Two-Hour Cancellation Window', content: 'Refund requests may be considered if the User emails the Company within 2 hours of payment AND the paid service has not yet been accessed, initiated, or fulfilled. No refund requests shall be entertained after the expiry of this 2-hour window.' },
      { heading: '4. Subscriptions', content: 'Users may cancel subscriptions at any time. Cancellation prevents future billing only. Current billing cycle remains non-refundable. Free trials convert automatically to paid subscriptions unless cancelled before expiry.' },
      { heading: '5. Refund Processing', content: 'Approved refunds will be processed within 7 business days via the original payment method. Transaction fees, gateway charges, or service delivery costs may be deducted.' },
      { heading: '6. Spiritual Outcomes', content: 'No refund shall be granted due to lack of perceived spiritual effectiveness, emotional dissatisfaction, differences in belief systems, or unmet life outcome expectations.' },
      { heading: '7. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ]
  },
  'cookie-policy': {
    icon: Cookie,
    title: 'Cookie Policy',
    effective: '18th February 2026',
    company: 'SkyHound Studios',
    sections: [
      { heading: '1. What Are Cookies', content: 'Cookies are small text files stored on your device when you access digital services. They enable platforms to recognize devices, remember preferences, and support functionality. We may also use local storage, pixel tags, SDK tracking tools, and device identifiers.' },
      { heading: '2. Types of Cookies We Use', content: 'We use strictly necessary cookies (authentication, security, payments), performance and analytics cookies (feature usage, navigation behavior), personalization cookies (customized insights, UI preferences), marketing and attribution cookies (referral tracking, campaign performance), and AI and behavioral optimization signals.' },
      { heading: '3. Your Cookie Choices', content: 'Users may manage cookie preferences through browser configuration settings, device privacy controls, or in-app consent or preference management tools. Disabling certain cookies may affect platform functionality, reduce personalization quality, or limit availability of certain features.' },
      { heading: '4. International Users', content: 'Users in certain jurisdictions (such as the European Union or United Kingdom) may have enhanced rights related to tracking technologies. We aim to comply with GDPR, ePrivacy Directive, and applicable global privacy regulation.' },
      { heading: '5. Contact', content: 'SkyHound Studios — Email: prateekmalhotra.contentcreator@gmail.com' },
    ]
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
            This page contains a summary of our {policy.title}. The complete legal document governing your use of our services 
            is available in full below. By using Everyday Horoscope, you agree to be bound by the complete terms.
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
              <div className="prose prose-sm max-w-none dark:prose-invert">
                <p className="text-xs text-muted-foreground mb-4">
                  Effective Date: {policy.effective} · Operated by: {policy.company}
                </p>
                {policy.fullText && policy.fullText.map((para, i) => (
                  <p key={i} className="text-sm text-muted-foreground leading-relaxed mb-3">{para}</p>
                ))}
              </div>
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
