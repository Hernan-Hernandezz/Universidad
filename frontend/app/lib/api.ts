const API_URL = process.env.NEXT_PUBLIC_API_URL;

// ─── Login ────────────────────────────────────────────────────
export const login = async (mail: string, password: string) => {
  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mail, password }),
    });
    return res.json();
  } catch (error) {
    console.error('Error login:', error);
  }
};

// ─── GET con token ────────────────────────────────────────────
export const fetchAPI = async (pathUrl: string, access_token: string) => {
  try {
    const res = await fetch(`${API_URL}${pathUrl}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify({ access_token }),
    });
    if (res.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return null;
    }
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
};

// ─── POST con token ───────────────────────────────────────────
export const postAPI = async (pathUrl: string, body: object, access_token: string) => {
  try {
    const res = await fetch(`${API_URL}${pathUrl}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify(body),
    });
    if (res.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return null;
    }
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
};

// ─── PUT con token ────────────────────────────────────────────
export const putAPI = async (pathUrl: string, body: object, access_token: string) => {
  try {
    const res = await fetch(`${API_URL}${pathUrl}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${access_token}`,
      },
      body: JSON.stringify(body),
    });
    if (res.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return null;
    }
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
};

// ─── DELETE con token ─────────────────────────────────────────
export const deleteAPI = async (pathUrl: string, access_token: string) => {
  try {
    const res = await fetch(`${API_URL}${pathUrl}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${access_token}`,
      },
    });
    if (res.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
      return null;
    }
    return res.json();
  } catch (err) {
    console.error(err);
    return null;
  }
};
