"use client";
import Link from "next/link";
import Exit from "../Components/Exit";

interface Props {
  children: any;
  href: string;
}
const ItemLink = ({ children, href }: Props) => {
  return (
    <li className="bg-secondary w-3/4 text-center p-2 rounded-lg">
      <Link href={href}>{children}</Link>
    </li>
  );
};
const Header = () => {
  return (
    <header className="h-screen w-40 bg-primary  text-white text-md capitalize flex flex-col justify-around">
      <nav className="h-3/4">
        <ul className="flex h-full gap-8 mt-8 items-center flex-col">
          <ItemLink href="/">dashboard</ItemLink>
          <ItemLink href="/horarios">horarios</ItemLink>
          <ItemLink href="/academico">academico</ItemLink>
          <ItemLink href="/comunicacion">comunicacion</ItemLink>
        </ul>
      </nav>
      <div className="h-1/4 flex justify-center items-center w-full">
        <Exit className="w-3/4" />
      </div>
    </header>
  );
};

export default Header;
