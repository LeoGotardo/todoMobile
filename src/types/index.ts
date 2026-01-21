export interface Todo {
  id: string;
  title: string;
  description: string;
  done: boolean;
  due_date: string | null;
  created_at: string;
}

export interface User {
  id: string;
  username: string;
  password: string;
}