create policy market_context_snapshots_service_role_all
on public.market_context_snapshots
for all
to service_role
using (true)
with check (true);
