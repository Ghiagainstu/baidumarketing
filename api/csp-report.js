module.exports = (req, res) => {
  // Only accept POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const report = req.body;
    const cspReport = report && report['csp-report'];
    
    if (cspReport) {
      const logData = {
        blocked: cspReport['blocked-uri'],
        violated: cspReport['violated-directive'],
        document: cspReport['document-uri'],
        line: cspReport['line-number'],
        timestamp: new Date().toISOString(),
      };
      
      // Log to Vercel console
      console.error('[CSP Violation]', JSON.stringify(logData));
    }
    
    // Return 204 No Content (CSP spec expects this)
    return res.status(204).end();
  } catch (err) {
    // Ignore parsing errors
    console.error('[CSP Report Parse Error]', err.message);
    return res.status(204).end();
  }
};
