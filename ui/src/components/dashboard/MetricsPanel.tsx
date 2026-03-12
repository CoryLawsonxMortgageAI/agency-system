import { useState } from 'react';
import { 
  TrendingUp, 
  TrendingDown, 
  Activity,
  Clock,
  Zap,
  Users,
  Download
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricCardProps {
  title: string;
  value: string;
  change: number;
  unit?: string;
  icon: React.ElementType;
  color: string;
}

function MetricCard({ title, value, change, unit, icon: Icon, color }: MetricCardProps) {
  const isPositive = change >= 0;
  
  return (
    <div className="p-5 bg-card rounded-xl border border-border">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-2xl font-bold mt-1">
            {value}
            {unit && <span className="text-sm font-normal text-muted-foreground ml-1">{unit}</span>}
          </p>
          <div className={cn(
            "flex items-center gap-1 mt-2 text-sm",
            isPositive ? "text-green-500" : "text-red-500"
          )}>
            {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
            <span>{isPositive ? '+' : ''}{change}%</span>
            <span className="text-muted-foreground text-xs ml-1">vs last hour</span>
          </div>
        </div>
        <div className={cn("p-3 rounded-xl", color)}>
          <Icon className="w-5 h-5 text-white" />
        </div>
      </div>
    </div>
  );
}

export function MetricsPanel() {
  const [timeRange, setTimeRange] = useState('1h');

  const metrics = [
    { title: 'API Requests', value: '24.5K', change: 12.5, unit: '/min', icon: Zap, color: 'bg-blue-500' },
    { title: 'Avg Response Time', value: '245', change: -8.2, unit: 'ms', icon: Clock, color: 'bg-green-500' },
    { title: 'Active Users', value: '1,429', change: 5.7, unit: '', icon: Users, color: 'bg-purple-500' },
    { title: 'Error Rate', value: '0.12', change: -15.3, unit: '%', icon: Activity, color: 'bg-red-500' },
  ];

  const timeRanges = ['1h', '6h', '24h', '7d', '30d'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">System Metrics</h2>
          <p className="text-muted-foreground">Performance analytics and monitoring</p>
        </div>
        
        <div className="flex items-center gap-3">
          {/* Time Range Selector */}
          <div className="flex bg-card rounded-lg p-1 border border-border">
            {timeRanges.map(range => (
              <button
                key={range}
                onClick={() => setTimeRange(range)}
                className={cn(
                  "px-3 py-1.5 rounded-md text-sm transition-colors",
                  timeRange === range 
                    ? "bg-primary text-primary-foreground" 
                    : "text-muted-foreground hover:text-foreground"
                )}
              >
                {range}
              </button>
            ))}
          </div>
          
          <button className="flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-lg hover:bg-accent transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {metrics.map(metric => (
          <MetricCard key={metric.title} {...metric} />
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Request Volume Chart */}
        <div className="p-6 bg-card rounded-xl border border-border">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold">Request Volume</h3>
              <p className="text-sm text-muted-foreground">API requests over time</p>
            </div>
            <Zap className="w-5 h-5 text-muted-foreground" />
          </div>
          
          <div className="h-64 flex items-end justify-between gap-1">
            {Array.from({ length: 24 }).map((_, i) => {
              const height = 30 + Math.random() * 60;
              return (
                <div
                  key={i}
                  className="flex-1 bg-primary/20 rounded-t hover:bg-primary/40 transition-colors relative group"
                  style={{ height: `${height}%` }}
                >
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-card px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity border whitespace-nowrap">
                    {Math.floor(height * 100)} req/min
                  </div>
                </div>
              );
            })}
          </div>
          
          <div className="flex justify-between mt-4 text-xs text-muted-foreground">
            <span>00:00</span>
            <span>06:00</span>
            <span>12:00</span>
            <span>18:00</span>
            <span>Now</span>
          </div>
        </div>

        {/* Response Time Chart */}
        <div className="p-6 bg-card rounded-xl border border-border">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="font-semibold">Response Time</h3>
              <p className="text-sm text-muted-foreground">Average latency (ms)</p>
            </div>
            <Clock className="w-5 h-5 text-muted-foreground" />
          </div>
          
          <div className="h-64 relative">
            {/* Line chart placeholder */}
            <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
                  <stop offset="0%" stopColor="rgb(59, 130, 246)" stopOpacity="0.3" />
                  <stop offset="100%" stopColor="rgb(59, 130, 246)" stopOpacity="0" />
                </linearGradient>
              </defs>
              
              {/* Area */}
              <path
                d={`M 0,${200 - 50} ${Array.from({ length: 20 }).map((_, i) => {
                  const x = (i + 1) * 20;
                  const y = 200 - (50 + Math.random() * 80);
                  return `L ${x},${y}`;
                }).join(' ')} L 400,200 L 0,200 Z`}
                fill="url(#gradient)"
              />
              
              {/* Line */}
              <path
                d={`M 0,${200 - 50} ${Array.from({ length: 20 }).map((_, i) => {
                  const x = (i + 1) * 20;
                  const y = 200 - (50 + Math.random() * 80);
                  return `L ${x},${y}`;
                }).join(' ')}`}
                fill="none"
                stroke="rgb(59, 130, 246)"
                strokeWidth="2"
              />
            </svg>
          </div>
          
          <div className="flex justify-between mt-4 text-xs text-muted-foreground">
            <span>00:00</span>
            <span>06:00</span>
            <span>12:00</span>
            <span>18:00</span>
            <span>Now</span>
          </div>
        </div>
      </div>

      {/* Agent Performance Table */}
      <div className="bg-card rounded-xl border border-border overflow-hidden">
        <div className="p-6 border-b border-border">
          <h3 className="font-semibold">Agent Performance</h3>
        </div>
        
        <table className="w-full">
          <thead className="bg-accent/50">
            <tr>
              <th className="text-left px-6 py-3 text-sm font-medium text-muted-foreground">Agent</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-muted-foreground">Tasks</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-muted-foreground">Avg Time</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-muted-foreground">Success Rate</th>
              <th className="text-left px-6 py-3 text-sm font-medium text-muted-foreground">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {[
              { name: 'Frontend Developer', tasks: 142, time: '2.3s', rate: '98%', status: 'active' },
              { name: 'Backend Architect', tasks: 89, time: '3.1s', rate: '96%', status: 'active' },
              { name: 'Content Creator', tasks: 234, time: '1.8s', rate: '99%', status: 'active' },
              { name: 'Growth Hacker', tasks: 67, time: '4.2s', rate: '94%', status: 'idle' },
              { name: 'AI Engineer', tasks: 45, time: '5.6s', rate: '92%', status: 'active' },
            ].map((agent, i) => (
              <tr key={i} className="hover:bg-accent/30 transition-colors">
                <td className="px-6 py-4 font-medium">{agent.name}</td>
                <td className="px-6 py-4 text-muted-foreground">{agent.tasks}</td>
                <td className="px-6 py-4 text-muted-foreground">{agent.time}</td>
                <td className="px-6 py-4">
                  <span className="text-green-500">{agent.rate}</span>
                </td>
                <td className="px-6 py-4">
                  <span className={cn(
                    "px-2 py-1 rounded-full text-xs",
                    agent.status === 'active' 
                      ? 'bg-green-500/20 text-green-500' 
                      : 'bg-gray-500/20 text-gray-500'
                  )}>
                    {agent.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
