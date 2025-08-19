import React from "react";

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center">
      <div className="w-full max-w-md px-4 pt-4 mx-auto flex flex-col gap-y-4">
        {/* Header */}
        <div className="flex items-center justify-between rounded-2xl bg-green-50 shadow-sm px-4 py-3">
          <div className="flex items-center gap-x-3">
            <span aria-label="Demeter logo" className="inline-block">
              <svg width={36} height={36} viewBox="0 0 36 36" fill="none" aria-hidden="true">
                <ellipse cx="18" cy="18" rx="16" ry="16" fill="#22c55e" />
                <path d="M18 8c-4.5 0-8 3.5-8 8 0 6.5 8 12 8 12s8-5.5 8-12c0-4.5-3.5-8-8-8zm0 10.5a2.5 2.5 0 110-5 2.5 2.5 0 010 5z" fill="#fff"/>
              </svg>
            </span>
            <div>
              <span className="text-lg font-bold text-green-700">Demeter</span>
              <div className="text-xs text-green-900">Agricultural AI Companion</div>
            </div>
          </div>
          <button
            aria-label="News"
            className="p-2 rounded-full bg-green-100 hover:bg-green-200 transition"
            type="button"
          >
            <svg width={24} height={24} fill="none" viewBox="0 0 24 24" aria-hidden="true">
              <rect x="3" y="5" width="18" height="14" rx="3" fill="#22c55e"/>
              <rect x="6" y="8" width="6" height="2" rx="1" fill="#fff"/>
              <rect x="6" y="12" width="12" height="2" rx="1" fill="#fff"/>
            </svg>
          </button>
        </div>

        {/* Hero */}
        <div className="rounded-2xl shadow-sm overflow-hidden relative w-full bg-gray-200" style={{ aspectRatio: "3 / 4" }}>
          <img
            src="/assets/images/farmer-tractor-field.jpg"
            alt="Farmer with tractor in green field at sunset"
            className="w-full h-full object-cover"
            draggable={false}
          />
          <button
            type="button"
            className="absolute bottom-4 left-4 bg-green-500 text-white font-semibold rounded-full px-6 py-2 shadow-md hover:bg-green-600 transition"
            style={{ minWidth: 120 }}
          >
            Get Started
          </button>
        </div>

        {/* Weather */}
        <div className="rounded-2xl bg-green-50 shadow-sm px-4 py-4 flex flex-col gap-y-3">
          <div className="flex items-center gap-x-2 mb-1">
            <span aria-label="Weather sun icon">
              <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                <circle cx="10" cy="10" r="5" fill="#fbbf24"/>
                <g stroke="#22c55e" strokeWidth="1.2">
                  <line x1="10" y1="1" x2="10" y2="3"/>
                  <line x1="10" y1="17" x2="10" y2="19"/>
                  <line x1="1" y1="10" x2="3" y2="10"/>
                  <line x1="17" y1="10" x2="19" y2="10"/>
                  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
                  <line x1="14.36" y1="14.36" x2="15.78" y2="15.78"/>
                  <line x1="4.22" y1="15.78" x2="5.64" y2="14.36"/>
                  <line x1="14.36" y1="5.64" x2="15.78" y2="4.22"/>
                </g>
              </svg>
            </span>
            <span className="font-semibold text-green-900 text-base">Weather (Last Updated: 2h ago)</span>
          </div>
          <div className="grid grid-cols-4 gap-x-2">
            <div className="flex flex-col items-center">
              <span aria-label="Temperature">
                <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                  <rect x="8" y="4" width="4" height="10" rx="2" fill="#ef4444"/>
                  <circle cx="10" cy="16" r="3" fill="#ef4444"/>
                </svg>
              </span>
              <span className="font-bold text-green-900 text-sm mt-1">28°C</span>
              <span className="text-xs text-green-800">Temp</span>
            </div>
            <div className="flex flex-col items-center">
              <span aria-label="Humidity">
                <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                  <ellipse cx="10" cy="12" rx="5" ry="7" fill="#38bdf8"/>
                </svg>
              </span>
              <span className="font-bold text-green-900 text-sm mt-1">65%</span>
              <span className="text-xs text-green-800">Humidity</span>
            </div>
            <div className="flex flex-col items-center">
              <span aria-label="Wind">
                <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                  <path d="M4 10h8a2 2 0 100-4" stroke="#64748b" strokeWidth="1.5" strokeLinecap="round"/>
                  <path d="M6 14h7a2 2 0 110 4" stroke="#64748b" strokeWidth="1.5" strokeLinecap="round"/>
                </svg>
              </span>
              <span className="font-bold text-green-900 text-sm mt-1">12 km/h</span>
              <span className="text-xs text-green-800">Wind</span>
            </div>
            <div className="flex flex-col items-center">
              <span aria-label="UV Index">
                <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                  <circle cx="10" cy="10" r="5" fill="#fbbf24"/>
                </svg>
              </span>
              <span className="font-bold text-green-900 text-sm mt-1">High</span>
              <span className="text-xs text-green-800">UV</span>
            </div>
          </div>
        </div>

        {/* News Section */}
        <div className="flex flex-col gap-y-3">
          <div className="flex items-center gap-x-2 mb-1">
            <span aria-label="News icon">
              <svg width={20} height={20} fill="none" viewBox="0 0 20 20" aria-hidden="true">
                <rect x="2" y="4" width="16" height="12" rx="2" fill="#22c55e"/>
                <rect x="5" y="7" width="5" height="1.5" rx="0.75" fill="#fff"/>
                <rect x="5" y="11" width="10" height="1.5" rx="0.75" fill="#fff"/>
              </svg>
            </span>
            <span className="font-semibold text-green-900 text-base">Agriculture News</span>
          </div>
          <div className="flex flex-col gap-y-2">
            {[
              {
                title: "Monsoon Arrives Early in South India",
                summary: "Farmers prepare for an early sowing season as the monsoon hits Kerala ahead of schedule.",
                img: "/assets/images/farmer-tractor-field.jpg"
              },
              {
                title: "New Subsidy Scheme Announced",
                summary: "Government introduces new credit subsidies for smallholder farmers.",
                img: "/assets/images/farmer-tractor-field.jpg"
              },
              {
                title: "Pest Alert: Armyworm Spotted",
                summary: "Agricultural department issues pest alert for maize crops in central India.",
                img: "/assets/images/farmer-tractor-field.jpg"
              }
            ].map((item, idx) => (
              <a
                key={item.title}
                href="#"
                className="flex items-center rounded-2xl bg-green-50 shadow-sm px-3 py-2 gap-x-3 hover:bg-green-100 transition"
                tabIndex={0}
                aria-label={`Read news: ${item.title}`}
              >
                <img
                  src={item.img}
                  alt="Agriculture news thumbnail"
                  className="w-12 h-12 rounded-xl object-cover flex-shrink-0"
                  draggable={false}
                />
                <div className="flex-1 min-w-0">
                  <div className="font-semibold text-green-900 text-sm truncate">{item.title}</div>
                  <div className="text-xs text-green-800 truncate">{item.summary}</div>
                </div>
                <span className="ml-2 text-green-500 font-medium text-xs flex items-center gap-x-1">
                  Read
                  <svg width={16} height={16} fill="none" viewBox="0 0 16 16" aria-hidden="true">
                    <path d="M6 4l4 4-4 4" stroke="#22c55e" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </span>
              </a>
            ))}
          </div>
        </div>
      </div>

      {/* Footer Nav */}
      <nav className="fixed bottom-0 left-0 right-0 w-full max-w-md mx-auto bg-white border-t border-gray-200 flex justify-between items-center px-6 py-2 z-10">
        <button aria-label="Home" className="flex flex-col items-center text-green-600">
          <span>🏠</span>
          <span className="text-xs">Home</span>
        </button>
        <button aria-label="Alerts" className="flex flex-col items-center text-green-600">
          <span>🔔</span>
          <span className="text-xs">Alerts</span>
        </button>
        <button aria-label="Voice" className="flex flex-col items-center text-green-600">
          <span>🎤</span>
          <span className="text-xs">Voice</span>
        </button>
        <button aria-label="Community" className="flex flex-col items-center text-green-600">
          <span>👥</span>
          <span className="text-xs">Community</span>
        </button>
        <button aria-label="Menu" className="flex flex-col items-center text-green-600">
          <span>☰</span>
          <span className="text-xs">Menu</span>
        </button>
      </nav>
    </div>
  );
}