import { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Workflow, 
  Zap, 
  Terminal, 
  Settings,
  Bot,
  Activity,
  Cpu,
  BarChart3,
  Shield,
  Sparkles,
  LogOut,
  User,
  Loader2
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { LoginPage } from '@/components/auth/LoginPage';
import { SystemOverview } from '@/components/dashboard/SystemOverview';
import { AgentsPanel } from '@/components/agents/AgentsPanel';
import { WorkflowsPanel } from '@/components/workflows/WorkflowsPanel';
import { TerminalPanel } from '@/components/dashboard/TerminalPanel';
import { AutonomousPanel } from '@/components/dashboard/AutonomousPanel';
import { MetricsPanel } from '@/components/dashboard/MetricsPanel';
import type { SystemStatus } from '@/types';

type Tab = 'overview' | 'agents' | 'workflows' | 'autonomous' | 'terminal' | 'metrics';

function SidebarItem({ 
  icon: Icon, 
  label, 
  active, 
  onClick,
  badge
}: { 
  icon: React.ElementType; 
  label: string; 
  active: boolean; 
  onClick: () => void;
  badge?: number;
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full flex items-center gap-3 px-4 py-3 text-sm font-medium transition-all duration-200 rounded-lg",
        active 
          ? "bg-primary/10 text-primary border-l-2 border-primary" 
          : "text-muted-foreground hover:bg-accent hover:text-foreground"
      )}
    >
      <Icon className={cn("w-5 h-5", active && "text-primary")} />
      <span>{label}</span>
      {badge !== undefined && badge > 0 && (
        <span className="ml-auto bg-primary text-primary-foreground text-xs px-2 py-0.5 rounded-full">
          {badge}
        </span>
      )}
    </button>
  );
}

// Simple hook for API calls
function useApiStatus() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const token = localStorage.getItem('agency_token');
        const headers: Record<string, string> = {};
        if (token) headers['Authorization'] = `Bearer ${token}`;
        
        const res = await fetch('/api/v1/system/status', { headers });
        if (res.ok) {
          const data = await res.json();
          setStatus(data);
        }
      } catch {
        // API not available
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return { status, loading };
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authLoading, setAuthLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tab>('overview');
  const { status } = useApiStatus();

  // Check for existing token on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('agency_token');
    if (savedToken) {
      // Validate token
      fetch('/api/v1/auth/me', {
        headers: { 'Authorization': `Bearer ${savedToken}` }
      })
      .then(res => {
        if (res.ok) {
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem('agency_token');
        }
      })
      .catch(() => {
        // API not available, but keep token for when it is
        setIsAuthenticated(true);
      })
      .finally(() => setAuthLoading(false));
    } else {
      setAuthLoading(false);
    }
  }, []);

  const handleLogin = (newToken: string) => {
    localStorage.setItem('agency_token', newToken);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('agency_token');
    setIsAuthenticated(false);
  };

  // Show loading while checking auth
  if (authLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-12 h-12 animate-spin text-primary" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // Show login page if not authenticated
  if (!isAuthenticated) {
    return <LoginPage onLogin={handleLogin} />;
  }

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <SystemOverview />;
      case 'agents':
        return <AgentsPanel />;
      case 'workflows':
        return <WorkflowsPanel />;
      case 'autonomous':
        return <AutonomousPanel />;
      case 'terminal':
        return <TerminalPanel />;
      case 'metrics':
        return <MetricsPanel />;
      default:
        return <SystemOverview />;
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-border">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-primary to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg">Agency</h1>
              <p className="text-xs text-muted-foreground">v1.0.0</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-4">
            Command Center
          </div>
          
          <SidebarItem 
            icon={LayoutDashboard} 
            label="Overview" 
            active={activeTab === 'overview'} 
            onClick={() => setActiveTab('overview')}
          />
          <SidebarItem 
            icon={Users} 
            label="Agents" 
            active={activeTab === 'agents'} 
            onClick={() => setActiveTab('agents')}
            badge={status?.active_agents}
          />
          <SidebarItem 
            icon={Workflow} 
            label="Workflows" 
            active={activeTab === 'workflows'} 
            onClick={() => setActiveTab('workflows')}
            badge={status?.active_workflows}
          />
          <SidebarItem 
            icon={Zap} 
            label="Autonomous" 
            active={activeTab === 'autonomous'} 
            onClick={() => setActiveTab('autonomous')}
          />
          
          <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mt-6 mb-3 px-4">
            Operations
          </div>
          
          <SidebarItem 
            icon={Terminal} 
            label="Terminal" 
            active={activeTab === 'terminal'} 
            onClick={() => setActiveTab('terminal')}
          />
          <SidebarItem 
            icon={BarChart3} 
            label="Metrics" 
            active={activeTab === 'metrics'} 
            onClick={() => setActiveTab('metrics')}
          />
          <SidebarItem 
            icon={Settings} 
            label="Settings" 
            active={false} 
            onClick={() => alert('Settings coming soon!')}
          />
        </nav>

        {/* User & Status Footer */}
        <div className="p-4 border-t border-border space-y-3">
          {/* User Info */}
          <div className="flex items-center gap-3 px-2">
            <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">Admin</p>
              <p className="text-xs text-muted-foreground">Administrator</p>
            </div>
            <button 
              onClick={handleLogout}
              className="p-2 hover:bg-accent rounded-lg transition-colors text-muted-foreground hover:text-red-500"
              title="Logout"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>

          {/* System Status */}
          <div className="flex items-center gap-2 text-xs px-2">
            <div className={cn(
              "w-2 h-2 rounded-full animate-pulse",
              status?.status === 'healthy' ? 'bg-green-500' : 'bg-yellow-500'
            )} />
            <span className="text-muted-foreground">
              {status?.status === 'healthy' ? 'System Online' : 'Connecting...'}
            </span>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 border-b border-border bg-card/50 backdrop-blur flex items-center justify-between px-6">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold capitalize">{activeTab}</h2>
          </div>
          
          <div className="flex items-center gap-4">
            {/* Quick Stats */}
            <div className="flex items-center gap-6 text-sm">
              <div className="flex items-center gap-2">
                <Cpu className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">CPU:</span>
                <span className="font-mono">{status?.metrics?.cpu_usage?.toFixed(1) || 0}%</span>
              </div>
              <div className="flex items-center gap-2">
                <Activity className="w-4 h-4 text-muted-foreground" />
                <span className="text-muted-foreground">Mem:</span>
                <span className="font-mono">{status?.metrics?.memory_usage?.toFixed(1) || 0}%</span>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-2">
              <button className="p-2 hover:bg-accent rounded-lg transition-colors">
                <Shield className="w-5 h-5 text-muted-foreground" />
              </button>
              <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
                <Sparkles className="w-4 h-4" />
                <span>New Task</span>
              </button>
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-auto bg-grid">
          <div className="p-6 animate-fade-in">
            {renderContent()}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
