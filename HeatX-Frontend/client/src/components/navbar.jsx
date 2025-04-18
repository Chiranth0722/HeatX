import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-800 px-4 py-3 shadow-md">
      <ul className="flex gap-6 text-white font-medium">
        <li><Link to="/">Home</Link></li>
        <li><Link to="/practice">Practice</Link></li>
        <li><Link to="/compare">Compare</Link></li>
        <li><Link to="/ecoscore">EcoScore</Link></li>
      </ul>
    </nav>
  );
}
