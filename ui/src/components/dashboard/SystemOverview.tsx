import { useApi } from '@/hooks/useApi';
import { SystemStatus } from '@/types';
import { 
  Bot, 
  Workflow, 
  Zap, 
  Clock, 
  TrendingUp, 
  AlertCircle,
  CheckCircle2,
  Activity
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { useState } from 'react';

function StatCard({ 
  title, 
  value, 
  subtitle, 
  icon: Icon, 
  trend,
  color = 'blue'
}: { 
  title: string; 
  value: string | number; 
  subtitle?: string;
  icon: React.ElementType;
  trend?: { value: number; positive: boolean };
  color?: 'blue' | 'green' | 'purple' | 'yellow' | 'red';
}) {
  const colorClasses = {
    blue: 'from-blue-500/20 to-blue-600/5 border-blue-500/30',
    green: 'from-green-500/20 to-green-600/5 border-green-500/30',
    purple: 'from-purple-500/20 to-purple-600/5 border-purple-500/30',
    yellow: 'from-yellow-500/20 to-yellow-600/5 border-yellow-500/30',
    red: 'from-red-500/20 to-red-600/5 border-red-500/30',
  };

  return (
    <div className={cn(
      "p-6 rounded-xl border bg-gradient-to-br",
      colorClasses[color]
    )}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold mt-2">{value}</p>
          {subtitle && (
            <p className="text-xs text-muted-foreground mt-1">{subtitle}</p>
          )}
        </div>
        <div className="p-3 bg-background/50 rounded-lg">
          <Icon className="w-5 h-5" />
        </div>
      </div>
      {trend && (
        <div className="mt-4 flex items-center gap-1 text-xs">
          <TrendingUp className={cn(
            "w-3 h-3",
            trend.positive ? "text-green-500" : "text-red-500"
          )} />
          <span className={trend.positive ? "text-green-500" : "text-red-500"}>
            {trend.positive ? '+' : ''}{trend.value}%
          </span>
          <span className="text-muted-foreground">vs last hour</span>
        </div>
      )}
    </div>
  );
}

function ActivityFeed() {
  const [activities] = useState([
    { id: 1, type: 'agent', message: 'Frontend Developer completed task', time: '2 min ago', icon: Bot },
    { id: 2, type: 'workflow', message: 'Marketing Campaign workflow started', time: '5 min ago', icon: Workflow },
    { id: 3, type: 'system', message: 'Autonomous mode activated', time: '10 min ago', icon: Zap },
    { id: 4, type: 'agent', message: 'Content Creator joined the swarm', time: '15 min ago', icon: Bot },
    { id: 5, type: 'system', message: 'System check passed', time: '20 min ago', icon: CheckCircle2 },
  ]);

  return (
    <div className="bg-card rounded-xl border border-border p-6">
      <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
      <div className="space-y-4">
        {activities.map((activity) => (
          <div key={activity.id} className="flex items-start gap-3">
            <div className="p-2 bg-accent rounded-lg">
              <activity.icon className="w-4 h-4 text-muted-foreground" />
            </div>
            <div className="flex-1">
              <p className="text-sm">{activity.message}</p>
              <p className="text-xs text-muted-foreground">{activity.time}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function HealthStatus() {
  const checks = [
    { name: 'API Server', status: 'operational', icon: Activity },
    { name: 'Agent Pool', status: 'operational', icon: Bot },
    { name: 'Workflow Engine', status: 'operational', icon: Workflow },
    { name: 'Database', status: 'operational', icon: Zap },
  ];

  return (
    <div className="bg-card rounded-xl border border-border p-6">
      <h3 className="text-lg font-semibold mb-4">System Health</h3>
      <div className="space-y-3">
        {checks.map((check) => (
          <div key={check.name} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <check.icon className="w-4 h-4 text-muted-foreground" />
              <span className="text-sm">{check.name}</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500" />
              <span className="text-xs text-muted-foreground capitalize">{check.status}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function SystemOverview() {
  const { data: status } = useApi<SystemStatus>('/system/status', 5000);

  return (
    <div className="space-y-6">
      {/* Welcome Banner */}
      <div className="p-8 rounded-2xl bg-gradient-to-r from-primary/20 via-purple-500/20 to-pink-500/20 border border-primary/30">
        <h1 className="text-3xl font-bold mb-2">🏢 Welcome to Agency</h1>
        <p className="text-muted-foreground max-w-2xl">
          Your autonomous AI agent swarm is operational. {status?.active_agents} agents are ready to execute tasks, 
          with {status?.active_workflows} active workflows running.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Active Agents"
          value={status?.active_agents || 0}
          subtitle={`of ${status?.total_agents || 0} total`}
          icon={Bot}
          color="blue"
          trend={{ value: 12, positive: true }}
        />
        <StatCard
          title="Active Workflows"
          value={status?.active_workflows || 0}
          subtitle={`${status?.queue_depth || 0} queued`}
          icon={Workflow}
          color="purple"
          trend={{ value: 8, positive: true }}
        />
        <StatCard
          title="Tasks Completed"
          value="1,247"
          subtitle="Last 24 hours"
          icon={CheckCircle2}
          color="green"
          trend={{ value: 23, positive: true }}
        />
        <StatCard
          title="Avg Response"
          value="2.3s"
          subtitle="API latency"
          icon={Clock}
          color="yellow"
          trend={{ value: 5, positive: false }}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-card rounded-xl border border-border p-6">
            <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-4">
              <button className="p-4 bg-accent/50 hover:bg-accent rounded-lg border border-border transition-all text-left group">
                <Bot className="w-8 h-8 mb-3 text-primary group-hover:scale-110 transition-transform" />
                <p className="font-medium">Deploy Agent</p>
                <p className="text-xs text-muted-foreground mt-1">Activate a new agent</p>
              </button>
              <button className="p-4 bg-accent/50 hover:bg-accent rounded-lg border border-border transition-all text-left group">
                <Workflow className="w-8 h-8 mb-3 text-purple-500 group-hover:scale-110 transition-transform" />
                <p className="font-medium">Run Workflow</p>
                <p className="text-xs text-muted-foreground mt-1">Execute multi-agent task</p>
              </button>
              <button className="p-4 bg-accent/50 hover:bg-accent rounded-lg border border-border transition-all text-left group">
                <Zap className="w-8 h-8 mb-3 text-yellow-500 group-hover:scale-110 transition-transform" />
                <p className="font-medium">Autonomous Mode</p>
                <p className="text-xs text-muted-foreground mt-1">Enable self-running ops</p>
              </button>
              <button className="p-4 bg-accent/50 hover:bg-accent rounded-lg border border-border transition-all text-left group">
                <AlertCircle className="w-8 h-8 mb-3 text-red-500 group-hover:scale-110 transition-transform" />
                <p className="font-medium">System Check</p>
                <p className="text-xs text-muted-foreground mt-1">Run diagnostics</p>
              </button>
            </div>
          </div>

          {/* Performance Chart Placeholder */}
          <div className="bg-card rounded-xl border border-border p-6">
            <h3 className="text-lg font-semibold mb-4">Performance Overview</h3>
            <div className="h-48 flex items-end justify-between gap-2">
              {[40, 65, 45, 80, 55, 70, 85, 60, 75, 90, 65, 80].map((height, i) => (
                <div
                  key={i}
                  className="flex-1 bg-primary/20 rounded-t hover:bg-primary/40 transition-colors relative group"
                  style={{ height: `${height}%` }}
                >
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-card px-2 py-1 rounded text-xs opacity-0 group-hover:opacity-100 transition-opacity border">
                    {height}%
                  </div>
                </div>
              ))}
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

        {/* Sidebar */}
        <div className="space-y-6">
          <HealthStatus />
          <ActivityFeed />
        </div>
      </div>
    </div>
  );
}
