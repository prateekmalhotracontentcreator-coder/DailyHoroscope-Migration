import axios from 'axios';

const BACKEND = process.env.REACT_APP_BACKEND_URL || '';

const normalizeUserId = (userId) => {
  if (!userId || typeof userId !== 'string') {
    return null;
  }
  const trimmed = userId.trim();
  return trimmed || null;
};

export const logEvent = (userId, eventType, pageUrl, metadata = {}) => {
  const resolvedUserId = normalizeUserId(userId);
  if (!resolvedUserId || !eventType || !pageUrl) {
    return;
  }

  axios.post(
    `${BACKEND}/api/diagnostics/log`,
    {
      user_id: resolvedUserId,
      event_type: eventType,
      page_url: pageUrl,
      metadata,
      timestamp: new Date().toISOString(),
    },
    { withCredentials: true }
  ).catch(() => {});
};

export const logPageView = (userId, pageUrl, prevUrl) => {
  logEvent(userId, 'PAGE_VIEW', pageUrl, {
    referrer: prevUrl || null,
  });
};

export const logRazorpayOpen = (userId, reportType, amount) => {
  logEvent(
    userId,
    'RAZORPAY_POPUP_OPEN',
    window.location.pathname,
    { reportType, amount }
  );
};
