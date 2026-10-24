-- reBottled: email sign-ups for the pilot
-- Run once in Supabase: Dashboard → SQL Editor → New query → paste → Run.
--
-- Security model
-- * The browser only knows the publishable key.
-- * The signups table has Row Level Security switched on and no policies, so
--   nobody can read, change or delete rows through the public API.
-- * The page writes only through upsert_signup(), which validates the input.
--   Read the sign-ups in the dashboard (Table Editor) or with the secret key.

create table if not exists public.signups (
  id          bigint generated always as identity primary key,
  email       text not null unique,          -- stored in lower case
  region      text check (region in ('malta', 'cyprus', 'canary-islands', 'other')),
  locale      text,                          -- page language: en, es, el, mt
  page        text,                          -- path the visitor signed up on
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table public.signups enable row level security;

-- Adds a sign-up, or updates the region/locale of an existing one.
-- Called twice from the page: first with the email, then with the island.
create or replace function public.upsert_signup(
  p_email  text,
  p_region text default null,
  p_locale text default null,
  p_page   text default null
)
returns void
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_email text := lower(trim(p_email));
begin
  if v_email is null
     or length(v_email) > 254
     or v_email !~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]{2,}$' then
    raise exception 'invalid email' using errcode = '22023';
  end if;

  if p_region is not null
     and p_region not in ('malta', 'cyprus', 'canary-islands', 'other') then
    raise exception 'invalid region' using errcode = '22023';
  end if;

  insert into public.signups (email, region, locale, page)
  values (v_email, p_region, left(p_locale, 10), left(p_page, 200))
  on conflict (email) do update
    set region     = coalesce(excluded.region, public.signups.region),
        locale     = coalesce(excluded.locale, public.signups.locale),
        updated_at = now();
end;
$$;

revoke all on function public.upsert_signup(text, text, text, text) from public;
grant execute on function public.upsert_signup(text, text, text, text) to anon, authenticated;
