// Surakshita - Dashboard Utilities

/**
 * Initialize the dashboard with all components
 */
function initializeDashboard() {
    console.log('Initializing Surakshita Dashboard...');
    
    // Check for geolocation support
    if (!navigator.geolocation) {
        console.warn('Geolocation is not supported by this browser.');
    }
    
    // Add event listeners
    setupEventListeners();
}

/**
 * Setup event listeners for dashboard interactions
 */
function setupEventListeners() {
    // Refresh data button (if implemented)
    const refreshBtn = document.getElementById('refreshData');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', refreshDashboardData);
    }
}

/**
 * Refresh dashboard data without page reload
 */
async function refreshDashboardData() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        // Update charts with new data
        updateCharts(data);
        
        console.log('Dashboard data refreshed successfully');
    } catch (error) {
        console.error('Error refreshing dashboard data:', error);
    }
}

/**
 * Update charts with new data
 */
function updateCharts(data) {
    // Implementation depends on chart instances
    console.log('Charts updated with new data:', data);
}

/**
 * Format date for display
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

/**
 * Format coordinates for display
 */
function formatCoordinates(lat, lng) {
    return `${parseFloat(lat).toFixed(6)}, ${parseFloat(lng).toFixed(6)}`;
}

/**
 * Get status badge color
 */
function getStatusColor(status) {
    return status === 'Pending' ? 'yellow' : 'green';
}

/**
 * Export incidents data to CSV
 */
async function exportToCSV() {
    try {
        const response = await fetch('/api/incidents');
        const incidents = await response.json();
        
        // Create CSV content
        const headers = ['ID', 'Type', 'Description', 'Latitude', 'Longitude', 'Status', 'Date'];
        const rows = incidents.map(inc => [
            inc.id,
            inc.incident_type,
            `"${inc.description.replace(/"/g, '""')}"`,
            inc.latitude,
            inc.longitude,
            inc.status,
            inc.created_at
        ]);
        
        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(','))
        ].join('\n');
        
        // Download CSV
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `surakshita_incidents_${new Date().toISOString().split('T')[0]}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        console.log('Incidents exported to CSV successfully');
    } catch (error) {
        console.error('Error exporting to CSV:', error);
    }
}

// Initialize on DOM load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeDashboard);
} else {
    initializeDashboard();
}
