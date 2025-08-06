// Performance monitoring utilities for Resume Scanner Frontend

class PerformanceMonitor {
  constructor() {
    this.metrics = {};
    this.startTime = performance.now();
  }

  // Measure page load time
  measurePageLoad() {
    window.addEventListener('load', () => {
      const loadTime = performance.now() - this.startTime;
      this.metrics.pageLoadTime = loadTime;
      
      // Navigation timing API
      if ('performance' in window) {
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
          this.metrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
          this.metrics.loadEvent = navigation.loadEventEnd - navigation.loadEventStart;
          this.metrics.firstPaint = this.getFirstPaint();
          this.metrics.firstContentfulPaint = this.getFirstContentfulPaint();
        }
      }
      
      this.logMetrics();
    });
  }

  // Get First Paint time
  getFirstPaint() {
    const paintEntries = performance.getEntriesByType('paint');
    const firstPaint = paintEntries.find(entry => entry.name === 'first-paint');
    return firstPaint ? firstPaint.startTime : null;
  }

  // Get First Contentful Paint time
  getFirstContentfulPaint() {
    const paintEntries = performance.getEntriesByType('paint');
    const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint');
    return fcp ? fcp.startTime : null;
  }

  // Measure component render time
  measureComponentRender(componentName, renderFunction) {
    const start = performance.now();
    const result = renderFunction();
    const end = performance.now();
    
    this.metrics[`${componentName}RenderTime`] = end - start;
    return result;
  }

  // Measure API call performance
  async measureApiCall(apiName, apiFunction) {
    const start = performance.now();
    try {
      const result = await apiFunction();
      const end = performance.now();
      this.metrics[`${apiName}Time`] = end - start;
      return result;
    } catch (error) {
      const end = performance.now();
      this.metrics[`${apiName}ErrorTime`] = end - start;
      throw error;
    }
  }

  // Log all metrics
  logMetrics() {
    console.group('🚀 Performance Metrics');
    console.table(this.metrics);
    
    // Performance recommendations
    this.generateRecommendations();
    console.groupEnd();
  }

  // Generate performance recommendations
  generateRecommendations() {
    const recommendations = [];
    
    if (this.metrics.pageLoadTime > 3000) {
      recommendations.push('⚠️ Page load time is slow (>3s). Consider code splitting and lazy loading.');
    }
    
    if (this.metrics.firstContentfulPaint > 2000) {
      recommendations.push('⚠️ First Contentful Paint is slow (>2s). Optimize critical rendering path.');
    }
    
    if (Object.keys(this.metrics).some(key => key.includes('RenderTime') && this.metrics[key] > 100)) {
      recommendations.push('⚠️ Some components are taking >100ms to render. Consider React.memo and useMemo.');
    }
    
    if (recommendations.length > 0) {
      console.group('💡 Performance Recommendations');
      recommendations.forEach(rec => console.log(rec));
      console.groupEnd();
    } else {
      console.log('✅ All performance metrics look good!');
    }
  }

  // Monitor memory usage
  monitorMemory() {
    if ('memory' in performance) {
      setInterval(() => {
        const memory = performance.memory;
        console.log('Memory Usage:', {
          used: Math.round(memory.usedJSHeapSize / 1048576) + ' MB',
          total: Math.round(memory.totalJSHeapSize / 1048576) + ' MB',
          limit: Math.round(memory.jsHeapSizeLimit / 1048576) + ' MB'
        });
      }, 10000); // Check every 10 seconds
    }
  }

  // Monitor long tasks
  monitorLongTasks() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 50) { // Tasks longer than 50ms
            console.warn('🐌 Long task detected:', {
              duration: Math.round(entry.duration) + 'ms',
              startTime: Math.round(entry.startTime) + 'ms'
            });
          }
        }
      });
      
      observer.observe({ entryTypes: ['longtask'] });
    }
  }
}

// Initialize performance monitoring
const performanceMonitor = new PerformanceMonitor();

// Start monitoring
performanceMonitor.measurePageLoad();
performanceMonitor.monitorMemory();
performanceMonitor.monitorLongTasks();

// Export for use in components
export default performanceMonitor; 