import api from "../axios";
import  type { BorrowedBook , OverdueBook} from "../types";


//  Get borrowed books
export const getMyBooks = () => {
  return api.get<BorrowedBook[]>("/user/mybooks");
};

//  Return a book by ISBN
export const returnBook = (isbn: string) => {
  return api.post(`/user/return/${isbn}`);
};

// Overdue books
export const getOverdueBooks = () => {
  return api.get<OverdueBook[]>("/user/mybooks/overdue");
};

// Borrow a book
export const borrowBook = (book_id: number) => {
  return api.post("/user/borrow", { book_id });
};
