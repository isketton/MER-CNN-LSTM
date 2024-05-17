import { render, screen } from "@testing-library/react";
import App, { FileInput } from "./pages/FileInput";

test("renders learn react link", () => {
  render(<FileInput />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
