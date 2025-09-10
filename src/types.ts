export interface Book {
  id: number;
  title: string;
  author: string;
  isbn: string;
  copies_available: number;
}

export interface BorrowedBook {
  id: number;
  book: Book;
  borrow_date: string;
  due_date: string;
  return_date: string | null;
}

export interface OverdueBookItem {
  user_name: string;
  email?: string;
  title: string;
  due_date: string;
  days_overdue: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

export interface ActiveUser {
  user_id: number;
  name: string;
  borrowed_count: number;
}

export interface ActiveUserBook {
  title: string;
  borrow_date: string;
  due_date: string;
  return_date: string | null;
}

export interface ActiveUser {
  id: number;
  name: string;
  email: string;
  role: string;
  borrowed_books: ActiveUserBook[];
}


export interface MostBorrowedBook {
  title: string;
  author: string;
  isbn: string;
  borrow_count: number;
}

export interface MonthlyUsageItem {
  book_title: string;
  user_name: string;
  borrow_date: string;
  return_date: string | null;
  overdue: boolean;
}
