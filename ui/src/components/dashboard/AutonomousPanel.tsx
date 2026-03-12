import { useState } from 'react';
import { 
  Zap, 
  Play, 
  Pause, 
  Settings, 
  Activity,
  TrendingUp,
  Bot,
  Brain,
  Target
} from 'lucide-react';
import { cn } from '@/lib/utils';

export function AutonomousPanel() {
  const [isActive, setIsActive] = useState(false);
  const [config, setConfig] = useState({
    scanInterval: 60,
    maxConcurrentTasks: 10,
    scalingThreshold: 500,
    autoDiscover: true,
    learningEnabled: true
  });

  const recentDecisions = [
    { id: 1, action: 'Scale Up', reason: 'Queue depth exceeded 500', time: '2 min ago', confidence: 92 },
    { id: 2, action: 'Optimize', reason: 'Low agent utilization detected', time: '15 min ago', confidence: 87 },
    { id: 3, action: 'Alert', reason: 'High error rate in workflow', time: '32 min ago', confidence: 95 },
    { id: 4, action: 'Deploy', reason: 'New content pipeline triggered', time: '1 hour ago', confidence: 89 },
  ];

  return (
    <div className="space-y-6">
      {/* Hero Section */}
      <div className={cn(
        "p-8 rounded-2xl border transition-all duration-500",
        isActive 
          ? "bg-gradient-to-r from-green-500/20 via-emerald-500/10 to-transparent border-green-500/30"
          : "bg-gradient-to-r from-yellow-500/20 via-orange-500/10 to-transparent border-yellow-500/30"
      )}>
        <div className="flex items-center justify-between">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <div className={cn(
                "p-3 rounded-xl transition-all duration-300",
                isActive ? "bg-green-500/20" : "bg-yellow-500/20"
              )}>
                <Brain className={cn(
                  "w-8 h-8",
                  isActive ? "text-green-500" : "text-yellow-500"
                )} />
              </div>
              <div>
                <h1 className="text-3xl font-bold">Autonomous Mode</h1>
                <p className="text-muted-foreground">
                  {isActive 
                    ? "🤖 System is self-managing and optimizing" 
                    : "⚠️ Autonomous operations are currently paused"}
                </p>
              </div>
            </div>
          </div>
          
          <button
            onClick={() => setIsActive(!isActive)}
            className={cn(
              "flex items-center gap-3 px-8 py-4 rounded-xl font-semibold text-lg transition-all duration-300",
              isActive 
                ? "bg-red-500/20 text-red-500 hover:bg-red-500/30"
                : "bg-green-500 text-white hover:bg-green-600 shadow-lg shadow-green-500/30"
            )}
          >
            {isActive ? (
              <><Pause className="w-6 h-6" /> Stop Autonomous Mode</>
            ) : (
              <><Play className="w-6 h-6" /> Start Autonomous Mode</>
            )}
          </button>
        </div>

        {isActive && (
          <div className="mt-6 grid grid-cols-4 gap-4 animate-fade-in">
            <div className="p-4 bg-background/50 rounded-xl border border-border">
              <div className="flex items-center gap-2 text-green-500 mb-1">
                <Activity className="w-4 h-4" />
                <span className="text-xs font-medium">MONITORING</span>
              </div>
              <p className="text-sm text-muted-foreground">Scanning every {config.scanInterval}s</p>
            </div>
            <div className="p-4 bg-background/50 rounded-xl border border-border">
              <div className="flex items-center gap-2 text-blue-500 mb-1">
                <Bot className="w-4 h-4" />
                <span className="text-xs font-medium">AGENTS</span>
              </div>
              <p className="text-sm text-muted-foreground">Max {config.maxConcurrentTasks} concurrent</p>
            </div>
            <div className="p-4 bg-background/50 rounded-xl border border-border">
              <div className="flex items-center gap-2 text-purple-500 mb-1">
                <TrendingUp className="w-4 h-4" />
                <span className="text-xs font-medium">SCALING</span>
              </div>
              <p className="text-sm text-muted-foreground">Trigger at {config.scalingThreshold} tasks</p>
            </div>
            <div className="p-4 bg-background/50 rounded-xl border border-border">
              <div className="flex items-center gap-2 text-yellow-500 mb-1">
                <Target className="w-4 h-4" />
                <span className="text-xs font-medium">LEARNING</span>
              </div>
              <p className="text-sm text-muted-foreground">{config.learningEnabled ? 'Enabled' : 'Disabled'}</p>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-card rounded-xl border border-border p-6">
            <div className="flex items-center gap-3 mb-6">
              <Settings className="w-5 h-5 text-primary" />
              <h3 className="text-lg font-semibold">Configuration</h3>
            </div>

            <div className="space-y-6">
              <div>
                <label className="text-sm font-medium mb-2 block">Scan Interval (seconds)</label>
                <input
                  type="range"
                  min="10"
                  max="300"
                  value={config.scanInterval}
                  onChange={(e) => setConfig({...config, scanInterval: parseInt(e.target.value)})}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>10s</span>
                  <span className="font-medium text-foreground">{config.scanInterval}s</span>
                  <span>300s</span>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Max Concurrent Tasks</label>
                <input
                  type="range"
                  min="1"
                  max="50"
                  value={config.maxConcurrentTasks}
                  onChange={(e) => setConfig({...config, maxConcurrentTasks: parseInt(e.target.value)})}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>1</span>
                  <span className="font-medium text-foreground">{config.maxConcurrentTasks}</span>
                  <span>50</span>
                </div>
              </div>

              <div>
                <label className="text-sm font-medium mb-2 block">Scaling Threshold (queue depth)</label>
                <input
                  type="range"
                  min="100"
                  max="2000"
                  step="100"
                  value={config.scalingThreshold}
                  onChange={(e) => setConfig({...config, scalingThreshold: parseInt(e.target.value)})}
                  className="w-full"
                />
                <div className="flex justify-between text-xs text-muted-foreground mt-1">
                  <span>100</span>
                  <span className="font-medium text-foreground">{config.scalingThreshold}</span>
                  <span>2000</span>
                </div>
              </div>

              <div className="flex items-center justify-between pt-4 border-t border-border">
                <div>
                  <p className="font-medium">Auto-Discover Tasks</p>
                  <p className="text-sm text-muted-foreground">Automatically detect and queue new tasks</p>
                </div>
                <button
                  onClick={() => setConfig({...config, autoDiscover: !config.autoDiscover})}
                  className={cn(
                    "w-12 h-6 rounded-full transition-colors relative",
                    config.autoDiscover ? "bg-primary" : "bg-muted"
                  )}
                >
                  <div className={cn(
                    "w-5 h-5 rounded-full bg-white absolute top-0.5 transition-all",
                    config.autoDiscover ? "left-6" : "left-0.5"
                  )} />
                </button>
              </div>

              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium">Continuous Learning</p>
                  <p className="text-sm text-muted-foreground">Improve decisions based on outcomes</p>
                </div>
                <button
                  onClick={() => setConfig({...config, learningEnabled: !config.learningEnabled})}
                  className={cn(
                    "w-12 h-6 rounded-full transition-colors relative",
                    config.learningEnabled ? "bg-primary" : "bg-muted"
                  )}
                >
                  <div className={cn(
                    "w-5 h-5 rounded-full bg-white absolute top-0.5 transition-all",
                    config.learningEnabled ? "left-6" : "left-0.5"
                  )} />
                </button>
              </div>
            </div>
          </div>

          {/* Metrics */}
          <div className="bg-card rounded-xl border border-border p-6">
            <h3 className="text-lg font-semibold mb-4">Performance Metrics</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="p-4 bg-accent/50 rounded-lg">
                <p className="text-2xl font-bold">247</p>
                <p className="text-sm text-muted-foreground">Decisions Made</p>
              </div>
              <div className="p-4 bg-accent/50 rounded-lg">
                <p className="text-2xl font-bold text-green-500">94%</p>
                <p className="text-sm text-muted-foreground">Success Rate</p>
              </div>
              <div className="p-4 bg-accent/50 rounded-lg">
                <p className="text-2xl font-bold">12</p>
                <p className="text-sm text-muted-foreground">Auto-Scaled</p>
              </div>
            </div>
          </div>
        </div>

        {/* Decision History */}
        <div className="bg-card rounded-xl border border-border p-6">
          <div className="flex items-center gap-3 mb-6">
            <Zap className="w-5 h-5 text-yellow-500" />
            <h3 className="text-lg font-semibold">Recent Decisions</h3>
          </div>

          <div className="space-y-4">
            {recentDecisions.map(decision => (
              <div key={decision.id} className="p-4 bg-accent/30 rounded-lg border border-border">
                <div className="flex items-start justify-between mb-2">
                  <div className={cn(
                    "px-2 py-1 rounded text-xs font-medium",
                    decision.action === 'Scale Up' ? 'bg-blue-500/20 text-blue-500' :
                    decision.action === 'Alert' ? 'bg-red-500/20 text-red-500' :
                    decision.action === 'Optimize' ? 'bg-green-500/20 text-green-500' :
                    'bg-purple-500/20 text-purple-500'
                  )}>
                    {decision.action}
                  </div>
                  <span className="text-xs text-muted-foreground">{decision.time}</span>
                </div>
                <p className="text-sm mb-2">{decision.reason}</p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-primary rounded-full"
                      style={{ width: `${decision.confidence}%` }}
                    />
                  </div>
                  <span className="text-xs text-muted-foreground">{decision.confidence}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
