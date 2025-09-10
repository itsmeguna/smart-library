// src/services/admin.ts
import api from "../axios";
import type { Book, User, ActiveUser, MostBorrowedBook, MonthlyUsageItem,OverdueBookItem } from "../types";

export const getAllBooks = () => api.get<Book[]>("/admin/books");

export const addBooks = (books: Book[]) =>
  api.post<Book[]>("/admin/books", books);

export const deleteBook = (isbn: string) =>
  api.delete(`/admin/books/${isbn}`);

export const getUsers = () => api.get<User[]>("/admin/users");

export const getActiveUsers = () => api.get<ActiveUser[]>("/admin/active-users");

export const getMostBorrowed = () => api.get<MostBorrowedBook[]>("/admin/most_borrowed");

export const getMonthlyUsage = (year: number, month: number) =>
  api.get<MonthlyUsageItem[]>("/admin/monthly_usage", { params: { year, month } });

export const getOverdueBooks = () => api.get<OverdueBookItem[]>("/admin/overdue-books");
