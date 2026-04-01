import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export async function submitTarotFeedback({ readingId, rating, comment }) {
  const res = await axios.post(
    `${API}/tarot/feedback`,
    {
      report_id: readingId,
      rating,
      comment,
    },
    { withCredentials: true }
  );
  return res.data;
}
