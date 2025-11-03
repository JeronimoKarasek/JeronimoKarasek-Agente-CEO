import { config } from './config.js';

export const supabase = self.supabase.createClient(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);

export const login = async (email, password) => {
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  return { user: data?.user, error };
};
export const logout = async () => { await supabase.auth.signOut(); };
export const getSession = async () => { const { data:{ session } } = await supabase.auth.getSession(); return session; };
