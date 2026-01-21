export class SocketClient {
  private host: string;
  private port: number;

  constructor(host: string = '192.168.0.29', port: number = 5000) {
    this.host = host;
    this.port = port;
  }

  async sendAndReceive(data: any): Promise<any> {
    try {
      const response = await fetch(`http://${this.host}:${this.port}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      return await response.json();
    } catch (error: any) {
      console.error('Socket error:', error);
      return { success: false, error: error.message || 'Erro de conexão' };
    }
  }
}