import axios from 'axios';

const API = `${process.env.REACT_APP_BACKEND_URL}/api/punya`;

export async function claimPunyaAction(actionCode, options = {}) {
  const payload = {
    action_code: actionCode,
    reference_id: options.referenceId || null,
    metadata: options.metadata || {},
  };
  const response = await axios.post(`${API}/actions/claim`, payload, {
    withCredentials: true,
  });
  return response.data;
}

export async function safeClaimPunyaAction(actionCode, options = {}) {
  try {
    return await claimPunyaAction(actionCode, options);
  } catch (error) {
    return {
      awarded: false,
      reason: error?.response?.data?.detail || "reward_unavailable",
      amount: 0,
    };
  }
}

export async function awardPunyaPoints(actionCode, options = {}) {
  return safeClaimPunyaAction(actionCode, options);
}

export async function fetchPunyaSummary() {
  const response = await axios.get(`${API}/summary`, { withCredentials: true });
  return response.data;
}

export async function fetchPunyaLedger(limit = 30) {
  const response = await axios.get(`${API}/ledger`, {
    params: { limit },
    withCredentials: true,
  });
  return response.data.transactions || [];
}

export async function fetchPunyaSpins(limit = 20) {
  const response = await axios.get(`${API}/spins`, {
    params: { limit },
    withCredentials: true,
  });
  return response.data.spins || [];
}

export async function fetchPunyaLeaderboard() {
  const response = await axios.get(`${API}/leaderboard`);
  return response.data;
}

export async function fetchPunyaPublicConfig() {
  const response = await axios.get(`${API}/config/public`);
  return response.data;
}

export async function spinPunyaWheel(spinMode = "auto") {
  const response = await axios.post(
    `${API}/spin`,
    { spin_mode: spinMode },
    { withCredentials: true },
  );
  return response.data;
}
