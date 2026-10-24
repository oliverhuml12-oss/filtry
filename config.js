// Public settings for the sign-up form.
//
// Both values are safe to publish: the publishable key can only call
// upsert_signup(), and the signups table itself is locked by Row Level
// Security (see supabase/schema.sql). Never put the secret key here.
//
// While these are empty, the form still works but nothing is saved
// (a warning is logged in the browser console).
window.REBOTTLED_CONFIG = {
  // Supabase → Project Settings → Data API → Project URL, e.g. "https://abcd1234.supabase.co"
  supabaseUrl: "",
  // Supabase → Project Settings → API Keys → Publishable key ("sb_publishable_…")
  supabaseKey: ""
};
