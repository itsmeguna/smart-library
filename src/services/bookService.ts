import api from "../axios";
import type { Book } from "../types";

//  Search books by title/author/isbn
export const searchBooks = (query: string) => {
  return api.get<Book[]>(`/books/search?q=${query}`);
};
