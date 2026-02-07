---
name: modern-ui-skill
description: Helps Claude design the best, modern, and market up-to-date user interfaces, leveraging the Context7 Skill for context awareness and the Skill Creator Skill for structuring new skills with current UI/UX best practices.
---
# Modern-UI-Skill

This skill enables Claude to design modern, responsive, and market-relevant user interfaces that align with current design trends and best practices.

## Purpose

The modern-ui-skill provides Claude with the capability to:
- Analyze project requirements using Context7 Skill for comprehensive understanding
- Generate modern, responsive UI designs aligned with current market trends
- Provide color schemes, typography, layout suggestions, and component recommendations
- Create actionable code snippets for popular front-end frameworks
- Apply skill creator methodology when structuring UI components as modular skills

## Instructions for Modern UI Design

### 1. Context Analysis with Context7
When analyzing UI requirements:
- Apply Context7 analysis to understand project scope and user needs
- Identify key elements, themes, and interconnections in requirements
- Extract actionable UI elements and user journey insights
- Maintain context continuity for consistent design language
- Note specific user interactions and accessibility requirements

### 2. Modern Design Principles
When creating UI designs:
- Follow current design trends (neumorphism, glassmorphism, brutalism, etc.) appropriately
- Apply clean, minimalist aesthetics with purposeful visual elements
- Ensure responsive design across all device sizes
- Implement accessibility best practices (WCAG 2.1 guidelines)
- Consider performance implications of design choices

### 3. Color and Typography
When selecting visual elements:
- Use modern color palettes (monochromatic, complementary, or gradient-based)
- Apply consistent typography hierarchy with appropriate font pairings
- Ensure sufficient contrast ratios for readability
- Consider brand alignment while maintaining modern aesthetics
- Use system fonts or optimized web fonts for performance

### 4. Component Recommendations
When suggesting UI components:
- Recommend reusable, modular components for consistency
- Focus on intuitive user interactions and micro-interactions
- Include data visualization components when needed (charts, graphs, etc.)
- Suggest appropriate animation and transition effects
- Consider mobile-first design approach

### 5. Code Implementation
When providing code examples:
- Use modern frameworks (React, Vue, Angular) with current best practices
- Implement Tailwind CSS, Material UI, or other popular styling libraries
- Include responsive design patterns and mobile considerations
- Provide accessibility attributes and semantic HTML
- Follow component architecture best practices

## Examples

### Example 1: SaaS Landing Page Design
**Input:**
```
Design a landing page UI for a SaaS product using modern best practices.
```

**Expected Output:**
```
## Analysis (Context7)
- Product: SaaS solution requiring clear value proposition
- Users: Business professionals seeking productivity tools
- Key elements: Hero section, features, testimonials, pricing, CTA

## Modern Design Approach
- Layout: Clean, asymmetrical design with generous whitespace
- Color scheme: Professional blue (#3B82F6) with neutral grays (#1F2937, #F9FAFB)
- Typography: Inter for headings, Open Sans for body text
- Visual elements: Subtle gradients, soft shadows, micro-interactions

## Implementation (React + Tailwind)
```jsx
import React from 'react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Navigation */}
      <nav className="flex items-center justify-between p-6">
        <div className="text-2xl font-bold text-gray-900">Brand</div>
        <div className="flex space-x-8">
          <a href="#" className="text-gray-600 hover:text-gray-900">Features</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Pricing</a>
          <a href="#" className="text-gray-600 hover:text-gray-900">Contact</a>
        </div>
        <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
          Get Started
        </button>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-20 text-center">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">
          Transform Your Business with Our SaaS Solution
        </h1>
        <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Powerful tools to help your team collaborate, innovate, and grow faster than ever before.
        </p>
        <div className="flex justify-center space-x-4">
          <button className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg hover:bg-blue-700 transition-colors">
            Start Free Trial
          </button>
          <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg text-lg hover:bg-gray-50 transition-colors">
            Watch Demo
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-6 py-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Feature cards would go here */}
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
```

## Verification
- Test responsive behavior across device sizes
- Validate accessibility with screen readers
- Confirm fast loading times and performance metrics
```

### Example 2: Dashboard UI with Analytics Data
**Input:**
```
Create a dashboard UI using context7 user analytics data.
```

**Expected Output:**
```
## Analysis (Context7)
- Data type: User analytics with metrics, trends, and KPIs
- Users: Data analysts and business stakeholders
- Key elements: Charts, tables, filters, real-time updates
- Context: Multiple data dimensions requiring visualization

## Modern Dashboard Design
- Layout: Grid-based with card components for modularity
- Color scheme: Professional palette with data visualization accents
- Typography: Clear hierarchy for data readability
- Interactions: Filter controls, drill-down capabilities, tooltips

## Implementation (React + Chart.js + Tailwind)
```jsx
import React, { useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

const Dashboard = ({ analyticsData }) => {
  const [timeRange, setTimeRange] = useState('7d');

  // Chart configurations would be defined here
  const lineChartConfig = {
    // Configuration for user activity chart
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Dashboard Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
          <div className="flex space-x-4">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 rounded-lg px-4 py-2"
            >
              <option value="24h">Last 24 hours</option>
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
            </select>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-gray-500 text-sm font-medium">Total Users</h3>
            <p className="text-3xl font-bold mt-2">{analyticsData.totalUsers}</p>
          </div>
          {/* Additional stat cards would follow */}
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4">User Activity</h3>
            <Line data={lineChartConfig} />
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Engagement by Channel</h3>
            <Bar data={barChartConfig} />
          </div>
        </div>

        {/* Data Table */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div className="p-6 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              {/* Table content would be defined here */}
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
```

## Verification
- Test chart rendering with different data sets
- Validate responsive behavior on various screen sizes
- Confirm data refresh and real-time update functionality
```

### Example 3: Mobile App UI Design
**Input:**
```
Generate mobile app UI design using current market UI trends.
```

**Expected Output:**
```
## Analysis (Context7)
- Platform: Mobile application with touch interactions
- Users: Mobile-first audience expecting intuitive experiences
- Key elements: Navigation, content consumption, personalization
- Trends: Glassmorphism, neumorphism, dark mode support

## Modern Mobile Design
- Layout: Bottom navigation, thumb-friendly touch targets
- Color scheme: Dark mode as default with vibrant accent colors
- Typography: Large, readable text with proper line height
- Interactions: Haptic feedback, smooth transitions, gesture support

## Implementation (React Native + Styled Components)
```jsx
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, SafeAreaView } from 'react-native';
import styled from 'styled-components/native';

const Container = styled(SafeAreaView)`
  flex: 1;
  background-color: #121212;
`;

const Header = styled.View`
  padding: 20px;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
`;

const GlassCard = styled.View`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 20px;
  margin: 10px;
  shadow-color: #000;
  shadow-offset: 0px 4px 6px;
  shadow-opacity: 0.1;
  shadow-radius: 10px;
`;

const MobileApp = () => {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <Container>
      <Header>
        <Text style={{ color: 'white', fontSize: 24, fontWeight: 'bold' }}>AppName</Text>
        <TouchableOpacity>
          <Text style={{ color: '#BB86FC', fontSize: 18 }}>Menu</Text>
        </TouchableOpacity>
      </Header>

      <ScrollView style={{ flex: 1 }}>
        {/* Featured Content */}
        <GlassCard>
          <Text style={{ color: 'white', fontSize: 18, fontWeight: 'bold', marginBottom: 10 }}>
            Featured Content
          </Text>
          <Text style={{ color: '#CCCCCC', fontSize: 14 }}>
            Discover the latest updates and recommendations
          </Text>
        </GlassCard>

        {/* Content Grid */}
        <View style={{ padding: 10 }}>
          {/* Content items would be mapped here */}
        </View>
      </ScrollView>

      {/* Bottom Navigation */}
      <View style={{ flexDirection: 'row', justifyContent: 'space-around', padding: 15, borderTopWidth: 1, borderTopColor: '#333' }}>
        <TouchableOpacity onPress={() => setActiveTab('home')}>
          <Text style={{ color: activeTab === 'home' ? '#BB86FC' : '#888', fontSize: 12 }}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('search')}>
          <Text style={{ color: activeTab === 'search' ? '#BB86FC' : '#888', fontSize: 12 }}>Search</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setActiveTab('profile')}>
          <Text style={{ color: activeTab === 'profile' ? '#BB86FC' : '#888', fontSize: 12 }}>Profile</Text>
        </TouchableOpacity>
      </View>
    </Container>
  );
};

export default MobileApp;
```

## Verification
- Test touch target sizes for accessibility
- Validate performance on various mobile devices
- Confirm proper navigation and user flow
```

## Guidelines for Using This Skill

### When to Activate
- When asked to design modern user interfaces
- When creating UI components that need to follow current trends
- When implementing responsive design solutions
- When generating code for UI frameworks
- When analyzing UI requirements using Context7

### Best Practices
- Always reference Context7 Skill for comprehensive requirement analysis
- Keep designs modern, clean, and aligned with current market trends
- Provide actionable code snippets for developers
- Consider accessibility and inclusive design principles
- Focus on performance and user experience optimization
- Apply modular component architecture when possible

### Response Structure
1. **Context Analysis**: Use Context7 to understand requirements
2. **Design Approach**: Outline modern design principles to apply
3. **Visual Elements**: Specify colors, typography, and layout
4. **Implementation**: Provide code examples for developers
5. **Verification**: Include testing and validation steps

### Quality Checks
- Does the design follow current UI/UX trends?
- Are accessibility guidelines properly implemented?
- Is the code clean, maintainable, and well-documented?
- Does the design work across different devices and screen sizes?
- Are performance considerations addressed?
- Is the user experience intuitive and engaging?

Use this skill whenever modern UI design assistance is needed, ensuring designs are current, accessible, and implementable with today's best practices.
