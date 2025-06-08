import { render, screen, waitFor } from '@testing-library/react';
import App from './App';
import { fetchAlerts, fetchTriageRules } from './api';

// Mock the API calls
jest.mock('./api');

describe('App Component', () => {
  const mockAlerts = [
    {
      id: 1,
      title: 'Test Alert',
      message: 'Test Message',
      status: 'firing',
      severity: 'critical'
    }
  ];

  const mockRules = [
    {
      id: 1,
      name: 'Test Rule',
      description: 'Test Description',
      priority: 1
    }
  ];

  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Setup mock implementations
    fetchAlerts.mockResolvedValue(mockAlerts);
    fetchTriageRules.mockResolvedValue(mockRules);
  });

  test('renders loading state initially', () => {
    render(<App />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('renders alerts and rules after loading', async () => {
    render(<App />);
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
    });

    // Check if alerts are displayed
    expect(screen.getByText('Test Alert')).toBeInTheDocument();
    expect(screen.getByText('critical')).toBeInTheDocument();

    // Check if rules are displayed
    expect(screen.getByText('Test Rule')).toBeInTheDocument();
    expect(screen.getByText('Test Description')).toBeInTheDocument();
  });

  test('handles API errors gracefully', async () => {
    // Mock API error
    fetchAlerts.mockRejectedValue(new Error('API Error'));
    
    render(<App />);
    
    // Wait for error message
    await waitFor(() => {
      expect(screen.getByText(/error/i)).toBeInTheDocument();
    });
  });
}); 