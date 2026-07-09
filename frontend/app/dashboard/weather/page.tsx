"use client";

import { useState } from "react";
import { FeatureShell } from "@/components/FeatureShell";
import { apiRequest, getLocation, reverseGeocode, ApiError } from "@/lib/api";
import {
  Loader2,
  AlertTriangle,
  Thermometer,
  Droplets,
  Wind,
  CloudRain,
  MapPin,
} from "lucide-react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

interface CurrentWeather {
  temperature?: number;
  humidity?: number;
  rain?: number;
  windSpeed?: number;
  cloudCover?: number;
}

interface ForecastDay {
  date: string;
  tempMax?: number;
  tempMin?: number;
  rain?: number;
}

interface DiseaseRisk {
  score?: number;
  level?: string;
  factors?: string[];
  recommendation?: string;
}

interface WeatherData {
  current?: CurrentWeather;
  forecast?: ForecastDay[];
  diseaseRisk?: DiseaseRisk;
}

const riskColor: Record<string, string> = {
  low: "bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900/40 dark:text-orange-300",
  critical: "bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300",
};

export default function WeatherPage() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<WeatherData | null>(null);
  const [place, setPlace] = useState<string | null>(null);

  async function loadWeather() {
    setLoading(true);
    setError(null);
    try {
      const { lat, lng } = await getLocation();
      setPlace(`${lat.toFixed(3)}, ${lng.toFixed(3)}`);
      // Resolve a friendly place name in the background (free, no API key)
      reverseGeocode(lat, lng).then(setPlace);
      const result = await apiRequest<WeatherData>(
        `/api/v1/weather/current?latitude=${lat}&longitude=${lng}&forecast_days=7`
      );
      setData(result);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  const chartData =
    data?.forecast?.map((d) => ({
      day: new Date(d.date).toLocaleDateString(undefined, { weekday: "short" }),
      max: d.tempMax,
      min: d.tempMin,
      rain: d.rain,
    })) ?? [];

  return (
    <FeatureShell
      title="Weather Intelligence"
      description="7-day forecast, disease-risk prediction, and irrigation guidance for your location."
    >
      {!data && !loading && (
        <div className="feature-card text-center py-10">
          <CloudRain className="w-12 h-12 mx-auto mb-4 text-blue-500" />
          <p className="text-gray-600 dark:text-gray-300 mb-6">
            We&apos;ll use your device location to fetch live weather. No API key
            needed.
          </p>
          <button
            onClick={loadWeather}
            className="rounded-full bg-green-600 text-white px-6 py-3 font-semibold hover:bg-green-700 inline-flex items-center gap-2"
          >
            <MapPin className="w-4 h-4" /> Get my weather
          </button>
        </div>
      )}

      {loading && (
        <div className="feature-card flex items-center justify-center py-16">
          <Loader2 className="w-6 h-6 animate-spin text-green-600 mr-2" />
          <span className="text-gray-600 dark:text-gray-300">
            Fetching live weather...
          </span>
        </div>
      )}

      {error && (
        <div
          role="alert"
          className="feature-card flex items-start gap-2 text-red-700 dark:text-red-300"
        >
          <AlertTriangle className="w-5 h-5 mt-0.5 shrink-0" />
          <div>
            <p>{error}</p>
            <button
              onClick={loadWeather}
              className="mt-2 text-sm underline hover:no-underline"
            >
              Try again
            </button>
          </div>
        </div>
      )}

      {data && (
        <div className="space-y-6">
          {place && (
            <p className="text-sm text-gray-500 flex items-center gap-1">
              <MapPin className="w-4 h-4" /> Location: {place}
            </p>
          )}

          {/* Current conditions */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              icon={<Thermometer className="w-5 h-5 text-orange-500" />}
              label="Temperature"
              value={fmt(data.current?.temperature, "°C")}
            />
            <StatCard
              icon={<Droplets className="w-5 h-5 text-blue-500" />}
              label="Humidity"
              value={fmt(data.current?.humidity, "%")}
            />
            <StatCard
              icon={<Wind className="w-5 h-5 text-teal-500" />}
              label="Wind"
              value={fmt(data.current?.windSpeed, " km/h")}
            />
            <StatCard
              icon={<CloudRain className="w-5 h-5 text-indigo-500" />}
              label="Rain"
              value={fmt(data.current?.rain, " mm")}
            />
          </div>

          {/* Disease risk */}
          {data.diseaseRisk && (
            <div className="feature-card">
              <div className="flex items-center gap-3 mb-3">
                <h3 className="text-lg font-bold">Disease Risk</h3>
                {data.diseaseRisk.level && (
                  <span
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      riskColor[data.diseaseRisk.level.toLowerCase()] ??
                      "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {data.diseaseRisk.level} ({data.diseaseRisk.score}/100)
                  </span>
                )}
              </div>
              {data.diseaseRisk.recommendation && (
                <p className="text-gray-700 dark:text-gray-300 mb-3">
                  {data.diseaseRisk.recommendation}
                </p>
              )}
              {data.diseaseRisk.factors &&
                data.diseaseRisk.factors.length > 0 && (
                  <ul className="space-y-1">
                    {data.diseaseRisk.factors.map((f, i) => (
                      <li
                        key={i}
                        className="text-sm text-gray-600 dark:text-gray-400 flex gap-2"
                      >
                        <span className="text-orange-500">⚠</span> {f}
                      </li>
                    ))}
                  </ul>
                )}
            </div>
          )}

          {/* Forecast chart */}
          {chartData.length > 0 && (
            <div className="feature-card">
              <h3 className="text-lg font-bold mb-4">7-Day Forecast</h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="max" name="Max °C" fill="#f97316" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="min" name="Min °C" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="rain" name="Rain mm" fill="#14b8a6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          <button
            onClick={loadWeather}
            className="text-sm text-green-600 hover:text-green-700 underline"
          >
            Refresh
          </button>
        </div>
      )}
    </FeatureShell>
  );
}

function fmt(value: number | undefined, unit: string): string {
  return value == null ? "--" : `${Math.round(value)}${unit}`;
}

function StatCard({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="feature-card">
      <div className="flex items-center gap-2 mb-1">{icon}</div>
      <p className="text-2xl font-bold text-gray-900 dark:text-white">{value}</p>
      <p className="text-sm text-gray-500">{label}</p>
    </div>
  );
}
