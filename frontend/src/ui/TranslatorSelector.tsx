interface TranslatorSelectorProps {
  value: string;
  onChange: (value: string) => void;
}

export default function TranslatorSelector({ value, onChange }: TranslatorSelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
        Translation Engine
      </label>
      <div className="flex gap-3">
        <button
          type="button"
          onClick={() => onChange('gemini')}
          className={`flex-1 px-4 py-3 rounded-lg border-2 transition-all duration-200 ${
            value === 'gemini'
              ? 'border-red-400 dark:border-red-500 bg-gradient-to-br from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 shadow-md'
              : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 hover:border-gray-400 dark:hover:border-gray-500'
          }`}
        >
          <div className="flex items-center gap-3">
            <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
              value === 'gemini'
                ? 'bg-red-400 dark:bg-red-500/80'
                : 'bg-gray-100 dark:bg-gray-700'
            }`}>
              <svg className={`w-6 h-6 ${value === 'gemini' ? 'text-white' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div className="flex-1 text-left">
              <div className={`font-semibold ${value === 'gemini' ? 'text-red-600 dark:text-red-400' : 'text-gray-900 dark:text-gray-100'}`}>
                Gemini Flash
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                LLM translation
              </div>
            </div>
            {value === 'gemini' && (
              <svg className="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            )}
          </div>
        </button>

        <button
          type="button"
          onClick={() => onChange('google')}
          className={`flex-1 px-4 py-3 rounded-lg border-2 transition-all duration-200 ${
            value === 'google'
              ? 'border-blue-500 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 shadow-md'
              : 'border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 hover:border-gray-400 dark:hover:border-gray-500'
          }`}
        >
          <div className="flex items-center gap-3">
            <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${
              value === 'google'
                ? 'bg-gradient-to-br from-blue-500 to-indigo-500'
                : 'bg-gray-100 dark:bg-gray-700'
            }`}>
              <svg className={`w-6 h-6 ${value === 'google' ? 'text-white' : 'text-gray-500'}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
            </div>
            <div className="flex-1 text-left">
              <div className={`font-semibold ${value === 'google' ? 'text-blue-600 dark:text-blue-400' : 'text-gray-900 dark:text-gray-100'}`}>
                Google Translate
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Relatively faster but unstable
              </div>
            </div>
            {value === 'google' && (
              <svg className="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
            )}
          </div>
        </button>
      </div>
    </div>
  );
}
