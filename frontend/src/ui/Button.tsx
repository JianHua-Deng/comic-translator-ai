import type { ReactNode } from "react";

interface ButtonProps {
  onClick: () => void;
  text?: string;
  variant?: "primary" | "secondary" | "ghost";
  size?: "sm" | "md";
  disabled?: boolean;
  loading?: boolean;
  className?: string;
  icon?: ReactNode;
}

export default function Button({
  onClick,
  text,
  variant = "primary",
  size = "md",
  disabled = false,
  loading = false,
  className = "",
  icon,
}: ButtonProps) {
  const base = "inline-flex items-center justify-center rounded transition focus:outline-none";
  const sizes: Record<string, string> = {
    sm: "px-3 py-1.5 text-sm h-8",
    md: "px-4 py-2 text-sm h-9",
  };
  const variants: Record<string, string> = {
    primary: "bg-red-400 text-white hover:bg-red-300",
    secondary: "bg-gray-100 text-gray-800 hover:bg-gray-200 border",
    ghost: "bg-transparent text-gray-800 hover:bg-gray-100",
  };

  const classes = `${base} ${sizes[size]} ${variants[variant]} ${
    disabled || loading ? "opacity-60 cursor-not-allowed" : "cursor-pointer"
  } ${className}`;

  return (
    <button
      onClick={onClick}
      className={classes}
      disabled={disabled || loading}
      type="button"
      aria-disabled={disabled || loading}
      aria-busy={loading}
    >
      {loading ? (
        <span className="mr-2 -ml-1 flex items-center">
          <svg
            className="animate-spin h-4 w-4 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        </span>
      ) : icon ? (
        <span className="mr-2 -ml-1 flex items-center">{icon}</span>
      ) : null}

      {text ? <span>{text}</span> : null}
    </button>
  );
}