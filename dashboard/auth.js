const SUPABASE_URL = 'https://gpakoffbuypbmfiwewka.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdwYWtvZmZidXlwYm1maXdld2thIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzI0ODA2NjAsImV4cCI6MjA0ODA1NjY2MH0.F9FsLxg8NA0nnYrYUnxPX7neXapNMEcBM2eM4ULztuc';
export const supabase = self.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

export const login = async (email, password) => {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  return { user: data?.user, error };
};
export const logout = async () => { await supabase.auth.signOut(); };
export const getSession = async () => { const { data:{ session } } = await supabase.auth.getSession(); return session; };
