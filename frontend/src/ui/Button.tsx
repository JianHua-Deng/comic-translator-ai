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
  const base = "inline-flex items-center justify-center rounded-lg font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 shadow-sm";
  const sizes: Record<string, string> = {
    sm: "px-4 py-2 text-sm h-9",
    md: "px-6 py-2.5 text-base h-11",
  };
  const variants: Record<string, string> = {
    primary: "bg-red-400 dark:bg-red-500/80 text-white hover:from-red-600 hover:to-pink-600 hover:shadow-lg hover:scale-105 focus:ring-red-500",
    secondary: "bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 border border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500 focus:ring-gray-500",
    ghost: "bg-transparent text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 focus:ring-gray-500",
  };

  const classes = `${base} ${sizes[size]} ${variants[variant]} ${
    disabled || loading ? "opacity-60 cursor-not-allowed hover:scale-100 hover:shadow-sm" : "cursor-pointer"
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
            className="animate-spin h-5 w-5 text-white"
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