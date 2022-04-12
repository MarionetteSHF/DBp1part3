from DBp1part3 import  create_app
app = create_app()
#
# if __name__ == '__main__':
#     app.run(debug=True, port=8111)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port

    # app.run(debug=True,host=HOST, port=PORT, debug=debug, threaded=threaded)
    app.run(debug=True, host=HOST, port=PORT, threaded=threaded)


  run()