// MongoDB Dummy Data: Analytics / Events DB
// This runs as the root user inside analytics_db

db = db.getSiblingDB('analytics_db');

// Create a dedicated user for this DB
db.createUser({
  user: 'admin',
  pwd: 'admin123',
  roles: [{ role: 'readWrite', db: 'analytics_db' }]
});

// ── Collection: users ─────────────────────────────────────────
db.users.insertMany([
  { _id: 1, username: 'alice91',   email: 'alice@web.com',  country: 'US', plan: 'pro',   joined: new Date('2023-01-15') },
  { _id: 2, username: 'bob_dev',   email: 'bob@web.com',    country: 'UK', plan: 'free',  joined: new Date('2023-06-20') },
  { _id: 3, username: 'carlos_mx', email: 'carlos@web.com', country: 'MX', plan: 'pro',   joined: new Date('2024-02-01') },
  { _id: 4, username: 'diana_fr',  email: 'diana@web.com',  country: 'FR', plan: 'team',  joined: new Date('2022-11-10') },
  { _id: 5, username: 'evan_cn',   email: 'evan@web.com',   country: 'CN', plan: 'team',  joined: new Date('2023-09-05') },
]);

// ── Collection: events ────────────────────────────────────────
db.events.insertMany([
  { user_id: 1, event: 'page_view',  page: '/dashboard',  ts: new Date('2026-03-01T10:00:00Z'), meta: { browser: 'Chrome', os: 'macOS' } },
  { user_id: 2, event: 'click',      page: '/pricing',    ts: new Date('2026-03-01T11:30:00Z'), meta: { button: 'upgrade' } },
  { user_id: 1, event: 'purchase',   page: '/checkout',   ts: new Date('2026-03-02T09:15:00Z'), meta: { amount: 49.99, currency: 'USD' } },
  { user_id: 3, event: 'page_view',  page: '/home',       ts: new Date('2026-03-03T08:00:00Z'), meta: { browser: 'Firefox', os: 'Linux' } },
  { user_id: 4, event: 'signup',     page: '/register',   ts: new Date('2026-03-04T14:22:00Z'), meta: { referral: 'google' } },
  { user_id: 5, event: 'logout',     page: '/settings',   ts: new Date('2026-03-05T17:00:00Z'), meta: {} },
]);

// ── Collection: reports ───────────────────────────────────────
db.reports.insertMany([
  { title: 'Q1 Traffic Summary',   created_at: new Date(), data: { visits: 120000, unique_users: 45000, bounce_rate: 0.38 } },
  { title: 'March Conversions',    created_at: new Date(), data: { conversions: 3200, revenue: 158400, avg_order: 49.5 } },
]);

print('✅ MongoDB: analytics_db loaded with users, events, reports');